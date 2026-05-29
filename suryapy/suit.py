"""
suryapy.suit
============

Functions for analysing solar UV/NB images from instruments like Aditya-L1 SUIT.
These complement the existing suryapy pipeline (b_roth, find_components, …) with
tools that work directly on FITS-loaded float arrays rather than DSLR JPEGs.

New public API
--------------
    load_suit_fits          Load and normalise a SUIT FITS file.
    detect_solar_disk       Robust radial-profile limb detection → mask, radius, centre.
    find_solar_center_fast  Down-sampled grid search for fast centre/radius estimation.
    radial_flatten          Divide every annulus by its median (removes limb darkening).
    extract_uv_features     Multiscale DoG feature map for UV structure detection.
    segment_uv_structures   Threshold + morphological cleanup → binary spot mask.
    detect_uv_structures    End-to-end: normalised image → labelled UV structures.
    plot_suit_pipeline      6-panel diagnostic figure (mirrors the notebook display).

Dependencies
------------
    numpy, scipy, matplotlib, astropy
    (no opencv, no scikit-image)

Usage example
-------------
    from suryapy.suit import load_suit_fits, detect_uv_structures, plot_suit_pipeline

    image = load_suit_fits("SUT_T26_…fits")
    result = detect_uv_structures(image)
    plot_suit_pipeline(result)
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import (
    gaussian_filter,
    gaussian_filter1d,
    median_filter,
    binary_opening,
    binary_closing,
    label,
)
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# I/O
# ─────────────────────────────────────────────────────────────────────────────

def load_suit_fits(
    path: str,
    hdu_index: int = 0,
    percentile_lo: float = 1.0,
    percentile_hi: float = 99.0,
) -> np.ndarray:
    """
    Load a SUIT FITS file and return a float array normalised to [0, 1].

    Parameters
    ----------
    path : str
        Path to the FITS file.
    hdu_index : int
        HDU extension that contains the image data (default 0).
    percentile_lo, percentile_hi : float
        Percentiles used for robust min/max normalisation.

    Returns
    -------
    image : ndarray, float64, shape (H, W)
        Normalised solar image in [0, 1].
    """
    from astropy.io import fits

    with fits.open(path) as hdul:
        data = hdul[hdu_index].data.astype(float)

    data = np.nan_to_num(data)
    lo = np.percentile(data, percentile_lo)
    hi = np.percentile(data, percentile_hi)
    data = np.clip((data - lo) / (hi - lo + 1e-12), 0.0, 1.0)
    return data


# ─────────────────────────────────────────────────────────────────────────────
# DISK DETECTION
# ─────────────────────────────────────────────────────────────────────────────

def _radial_median_profile(
    image: np.ndarray,
    cx: float,
    cy: float,
    clean_sector: Optional[np.ndarray] = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the median radial profile of *image* centred on (cx, cy).

    Returns
    -------
    r_map   : float array, same shape as image — distance from (cx, cy)
    profile : 1-D float array of length ceil(max_r)
    """
    h, w = image.shape
    y_idx, x_idx = np.indices(image.shape)
    r_map = np.sqrt((x_idx - cx) ** 2 + (y_idx - cy) ** 2)
    r_int = r_map.astype(int)
    max_r = int(r_map.max()) + 1

    profile = np.zeros(max_r)
    for rad in range(max_r):
        mask = r_int == rad
        if clean_sector is not None:
            mask = mask & clean_sector
        if np.any(mask):
            profile[rad] = np.median(image[mask])

    return r_map, profile


def detect_solar_disk(
    image: np.ndarray,
    smooth_sigma: float = 10.0,
    clean_sector_angles: tuple[float, float] = (-2.4, 1.8),
    print_log: bool = False,
) -> dict:
    """
    Detect the solar limb from a normalised image using the robust radial-profile
    method.  Works well on SUIT NB images where off-disk artefacts are present
    in some angular sectors.

    Algorithm
    ---------
    1. Build a polar-coordinate grid centred on the image centre.
    2. Restrict the radial profile to a "clean sector" (avoids bright artefacts).
    3. Smooth the profile with a 1-D Gaussian.
    4. Find the solar radius as the location of the steepest negative gradient
       (sharpest limb transition).
    5. Build a boolean solar mask and a radially-flattened image.

    Parameters
    ----------
    image : ndarray, float
        Normalised solar image (output of ``load_suit_fits`` or equivalent).
    smooth_sigma : float
        Sigma (pixels) for Gaussian smoothing of the radial profile.
    clean_sector_angles : (lo, hi) in radians
        Angular range (arctan2 convention) used to build the radial profile.
        Default avoids the typical SUIT off-disk bright stripe.
    print_log : bool
        Print estimated radius to stdout.

    Returns
    -------
    dict with keys:
        cx, cy      : float  — image centre used (pixels)
        R           : int    — estimated solar radius (pixels)
        solar_mask  : bool ndarray (H, W)
        masked      : float ndarray (H, W) — image inside disk, zero outside
        r_map       : float ndarray (H, W) — pixel distance from centre
        profile_raw : 1-D array — raw radial median profile
        profile_smooth : 1-D array — smoothed profile
    """
    h, w = image.shape
    cx = w // 2
    cy = h // 2

    y_idx, x_idx = np.indices(image.shape)
    theta = np.arctan2(y_idx - cy, x_idx - cx)

    lo_ang, hi_ang = clean_sector_angles
    clean_sector = (theta > lo_ang) & (theta < hi_ang)

    r_map, profile_raw = _radial_median_profile(image, cx, cy, clean_sector)

    profile_smooth = gaussian_filter1d(profile_raw, sigma=smooth_sigma)
    deriv = np.gradient(profile_smooth)
    R = int(np.argmin(deriv))

    solar_mask = r_map <= R
    masked = np.zeros_like(image)
    masked[solar_mask] = image[solar_mask]

    if print_log:
        print(f"[detect_solar_disk] Centre = ({cx}, {cy})  Radius = {R} px")

    return {
        "cx": cx,
        "cy": cy,
        "R": R,
        "solar_mask": solar_mask,
        "masked": masked,
        "r_map": r_map,
        "profile_raw": profile_raw,
        "profile_smooth": profile_smooth,
    }


def find_solar_center_fast(
    image: np.ndarray,
    downsample: int = 8,
    search_half: int = 30,
    search_step: int = 2,
    smooth_sigma: float = 4.0,
    edge_fraction: float = 0.4,
    print_log: bool = False,
) -> dict:
    """
    Fast solar centre and radius estimation via downsampled grid search.

    Scans a coarse grid of candidate centres around the image midpoint,
    scores each by the sharpness of the radial limb transition, and
    returns the best-scoring candidate (scaled back to full resolution).

    Parameters
    ----------
    image : ndarray, float
        Full-resolution normalised image.
    downsample : int
        Spatial downsampling factor (8 → 8× smaller image for the search).
    search_half : int
        Half-width of the search grid in down-sampled pixels.
    search_step : int
        Step size of the grid scan.
    smooth_sigma : float
        Gaussian sigma for profile smoothing (down-sampled pixels).
    edge_fraction : float
        Fraction of minimum derivative used as threshold to find the limb
        candidate in each trial profile.
    print_log : bool
        Print result to stdout.

    Returns
    -------
    dict with keys:
        cx, cy : int — best centre (full-resolution pixels)
        R      : int — best radius estimate (full-resolution pixels)
    """
    small = image[::downsample, ::downsample]
    h_s, w_s = small.shape
    y_s, x_s = np.indices(small.shape)

    cx0, cy0 = w_s // 2, h_s // 2

    best_score = -np.inf
    best_cx = cx0
    best_cy = cy0
    best_R = 0

    for dx in range(-search_half, search_half, search_step):
        for dy in range(-search_half, search_half, search_step):
            cx = cx0 + dx
            cy = cy0 + dy

            rr = np.sqrt((x_s - cx) ** 2 + (y_s - cy) ** 2)
            rr_int = rr.astype(np.int32)
            max_r = int(rr_int.max())

            profile = np.zeros(max_r)
            for rad in range(max_r):
                vals = small[rr_int == rad]
                if vals.size > 0:
                    profile[rad] = np.median(vals)

            smooth = gaussian_filter1d(profile, sigma=smooth_sigma)
            deriv = np.gradient(smooth)

            score = float(np.abs(np.min(deriv)))

            threshold = edge_fraction * np.min(deriv)
            candidates = np.where(deriv < threshold)[0]
            if candidates.size == 0:
                continue
            R_candidate = int(candidates[0])

            if score > best_score:
                best_score = score
                best_cx = cx
                best_cy = cy
                best_R = R_candidate

    # Scale back to full resolution
    best_cx *= downsample
    best_cy *= downsample
    best_R *= downsample

    if print_log:
        print(
            f"[find_solar_center_fast] Centre = ({best_cx}, {best_cy})"
            f"  Radius = {best_R} px"
        )

    return {"cx": best_cx, "cy": best_cy, "R": best_R}


# ─────────────────────────────────────────────────────────────────────────────
# RADIAL FLATTENING
# ─────────────────────────────────────────────────────────────────────────────

def radial_flatten(
    image: np.ndarray,
    r_map: np.ndarray,
    solar_mask: np.ndarray,
    profile_smooth: np.ndarray,
) -> np.ndarray:
    """
    Remove large-scale radial intensity variation (limb darkening / vignetting)
    by dividing each annulus by its smoothed median value.

    Parameters
    ----------
    image : ndarray (H, W)
        Input image (values inside the solar disk are processed).
    r_map : ndarray (H, W)
        Pixel distance from the solar centre (from ``detect_solar_disk``).
    solar_mask : bool ndarray (H, W)
        True inside the solar disk.
    profile_smooth : 1-D array
        Smoothed radial median profile (from ``detect_solar_disk``).

    Returns
    -------
    flattened : ndarray (H, W), normalised to [0, 1] inside the disk.
    """
    r_int = r_map.astype(int)
    max_r = len(profile_smooth)
    flattened = np.zeros_like(image)

    for rad in range(max_r):
        annulus = (r_int == rad) & solar_mask
        if np.any(annulus):
            val = profile_smooth[rad]
            if val > 0:
                flattened[annulus] = image[annulus] / val

    # Normalise to [0, 1]
    disk_vals = flattened[solar_mask]
    if disk_vals.ptp() > 0:
        flattened[solar_mask] = (disk_vals - disk_vals.min()) / disk_vals.ptp()

    return flattened


# ─────────────────────────────────────────────────────────────────────────────
# UV FEATURE EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

def extract_uv_features(
    flattened: np.ndarray,
    sigma_small: float = 2.0,
    sigma_large: float = 20.0,
    median_size: int = 5,
    final_sigma: float = 1.0,
) -> np.ndarray:
    """
    Build a multiscale difference-of-Gaussians (DoG) feature map that
    highlights compact dark structures (sunspots, plage boundaries, filaments)
    in a radially-flattened solar image.

    Parameters
    ----------
    flattened : ndarray (H, W)
        Radially-flattened solar image (output of ``radial_flatten``).
    sigma_small : float
        Small-scale Gaussian sigma (preserves fine structure).
    sigma_large : float
        Large-scale Gaussian sigma (models the smooth background).
    median_size : int
        Median filter size applied after DoG subtraction to reduce salt-and-
        pepper noise.
    final_sigma : float
        Final light Gaussian smoothing sigma.

    Returns
    -------
    features : ndarray (H, W), normalised to [0, 1].
    """
    small_blur = gaussian_filter(flattened, sigma=sigma_small)
    large_blur = gaussian_filter(flattened, sigma=sigma_large)
    features = small_blur - large_blur

    features = median_filter(features, size=median_size)
    features = gaussian_filter(features, sigma=final_sigma)

    # Normalise
    fmin, fmax = features.min(), features.max()
    if fmax > fmin:
        features = (features - fmin) / (fmax - fmin)

    return features


def segment_uv_structures(
    features: np.ndarray,
    solar_mask: np.ndarray,
    dark_percentile: float = 8.0,
    opening_struct_size: int = 3,
    closing_struct_size: int = 5,
) -> np.ndarray:
    """
    Threshold the feature map to isolate dark UV structures and apply
    morphological cleanup.

    Parameters
    ----------
    features : ndarray (H, W)
        Output of ``extract_uv_features``.
    solar_mask : bool ndarray (H, W)
        Pixels inside the solar disk.
    dark_percentile : float
        Features below this percentile of disk pixels are labelled as
        dark structures.  Lower value → stricter / fewer detections.
    opening_struct_size : int
        Side of the square structuring element for binary opening
        (removes small speckles).
    closing_struct_size : int
        Side of the square structuring element for binary closing
        (fills small holes).

    Returns
    -------
    spots : bool ndarray (H, W) — True where a dark UV structure is detected.
    """
    threshold = np.percentile(features[solar_mask], dark_percentile)
    spots = (features < threshold) & solar_mask

    spots = binary_opening(spots, structure=np.ones((opening_struct_size,) * 2))
    spots = binary_closing(spots, structure=np.ones((closing_struct_size,) * 2))

    return spots.astype(bool)


def detect_uv_structures(
    image: np.ndarray,
    disk_smooth_sigma: float = 10.0,
    clean_sector_angles: tuple[float, float] = (-2.4, 1.8),
    sigma_small: float = 2.0,
    sigma_large: float = 20.0,
    dark_percentile: float = 8.0,
    print_log: bool = False,
) -> dict:
    """
    End-to-end pipeline: normalised image → labelled UV dark structures.

    This is the high-level convenience wrapper that chains
    ``detect_solar_disk`` → ``radial_flatten`` → ``extract_uv_features``
    → ``segment_uv_structures`` → ``scipy.ndimage.label``.

    Parameters
    ----------
    image : ndarray (H, W)
        Normalised solar image (use ``load_suit_fits`` for FITS input).
    disk_smooth_sigma : float
        Passed to ``detect_solar_disk``.
    clean_sector_angles : (lo, hi) in radians
        Passed to ``detect_solar_disk``.
    sigma_small, sigma_large : float
        Passed to ``extract_uv_features``.
    dark_percentile : float
        Passed to ``segment_uv_structures``.
    print_log : bool
        Print progress messages.

    Returns
    -------
    dict with keys:
        image         : original input image
        disk          : dict from detect_solar_disk (cx, cy, R, masks, …)
        flattened     : radially-flattened image
        features      : multiscale feature map
        spots         : binary spot mask
        labeled       : labeled integer array
        n_components  : int — number of detected UV structures
    """
    disk = detect_solar_disk(
        image,
        smooth_sigma=disk_smooth_sigma,
        clean_sector_angles=clean_sector_angles,
        print_log=print_log,
    )

    flattened = radial_flatten(
        image,
        r_map=disk["r_map"],
        solar_mask=disk["solar_mask"],
        profile_smooth=disk["profile_smooth"],
    )

    features = extract_uv_features(
        flattened,
        sigma_small=sigma_small,
        sigma_large=sigma_large,
    )

    spots = segment_uv_structures(
        features,
        solar_mask=disk["solar_mask"],
        dark_percentile=dark_percentile,
    )

    labeled, n_components = label(spots)

    if print_log:
        print(f"[detect_uv_structures] Detected {n_components} UV structures.")

    return {
        "image": image,
        "disk": disk,
        "flattened": flattened,
        "features": features,
        "spots": spots,
        "labeled": labeled,
        "n_components": n_components,
    }


# ─────────────────────────────────────────────────────────────────────────────
# VISUALISATION
# ─────────────────────────────────────────────────────────────────────────────

def plot_suit_pipeline(
    result: dict,
    figsize: tuple[int, int] = (18, 12),
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    6-panel diagnostic figure showing each stage of the SUIT pipeline.

    Panels
    ------
    [0,0] Original image
    [0,1] Radial profile (raw + smooth) with limb marker
    [0,2] Detected solar disk (mask overlay + circle)
    [1,0] Radially-flattened image
    [1,1] Multiscale feature map (inferno colormap)
    [1,2] Original image with UV structure contours (cyan)

    Parameters
    ----------
    result : dict
        Output of ``detect_uv_structures``.
    figsize : (width, height)
    save_path : str or None
        If given, save the figure to this path.

    Returns
    -------
    fig : matplotlib Figure
    """
    image    = result["image"]
    disk     = result["disk"]
    flat     = result["flattened"]
    features = result["features"]
    spots    = result["spots"]

    cx, cy = disk["cx"], disk["cy"]
    R      = disk["R"]
    prof_r = disk["profile_raw"]
    prof_s = disk["profile_smooth"]

    fig, ax = plt.subplots(2, 3, figsize=figsize)

    # --- Original image ---
    ax[0, 0].imshow(image, cmap="gray", origin="upper")
    ax[0, 0].set_title("Original SUIT Image")

    # --- Radial profile ---
    ax[0, 1].plot(prof_r, alpha=0.5, label="raw")
    ax[0, 1].plot(prof_s, linewidth=2.5, label="smooth")
    ax[0, 1].axvline(R, color="red", linewidth=1.5, label=f"R = {R} px")
    ax[0, 1].set_title("Radial Profile")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].set_xlabel("radius (px)")

    # --- Detected solar disk ---
    ax[0, 2].imshow(disk["masked"], cmap="gray", origin="upper")
    circle = plt.Circle((cx, cy), R, color="red", fill=False, linewidth=1.5)
    ax[0, 2].add_patch(circle)
    ax[0, 2].scatter(cx, cy, s=30, c="red", zorder=5)
    ax[0, 2].set_title(f"Detected Solar Disk  R={R} px")

    # --- Radially flattened ---
    ax[1, 0].imshow(flat, cmap="gray", origin="upper")
    ax[1, 0].set_title("Radial Flattening")

    # --- Feature map ---
    ax[1, 1].imshow(features, cmap="inferno", origin="upper")
    ax[1, 1].set_title("Multiscale Features (DoG)")

    # --- UV structure contours ---
    ax[1, 2].imshow(image, cmap="gray", origin="upper")
    ax[1, 2].contour(spots, colors="cyan", linewidths=0.6)
    ax[1, 2].set_title(f"Detected UV Structures  (n={result['n_components']})")

    for a in ax.ravel():
        a.axis("off")
    ax[0, 1].axis("on")  # keep axes on the profile plot

    plt.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig
