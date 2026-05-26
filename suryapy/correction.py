"""
Limb darkening correction.

Implements the polynomial radial-profile correction from the internship
notebook: for each radius r, compute the median intensity of all pixels
at that radius, fit a 3rd-degree polynomial, then divide each pixel by
its fitted profile value.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def _polynomial_3rd_degree(r, a, b, c, d):
    """Third-degree polynomial used for the radial intensity fit."""
    return a * r**3 + b * r**2 + c * r + d


def limb_darkening_correction(image, show_plot=False):
    """
    Correct for limb darkening using a radial median intensity profile.

    For each integer radius from the image centre, the median pixel
    intensity is computed. A 3rd-degree polynomial is fitted to this
    profile, and every pixel is divided by the fitted value at its
    radius to produce a flat (corrected) image.

    Parameters
    ----------
    image : np.ndarray
        2D grayscale image (float or int). Typically the output of
        mask_sun or a gaussian-filtered crop.
    show_plot : bool, optional
        If True, display the corrected image. Default is False.

    Returns
    -------
    corrected_image : np.ndarray
        Float array, same shape as image, with limb darkening removed.

    Examples
    --------
    >>> from astrolab import imaging as im
    >>> from scipy import ndimage as scp
    >>> from sunspots.correction import limb_darkening_correction
    >>> crop = ...   # result of mask_sun
    >>> gauss = scp.gaussian_filter(crop, sigma=0.5, radius=2)
    >>> corrected = limb_darkening_correction(gauss)
    """
    image = image.astype(float)
    h, w = image.shape
    center_x, center_y = w // 2, h // 2

    y_idx, x_idx = np.indices((h, w))
    radii = np.sqrt((x_idx - center_x)**2 + (y_idx - center_y)**2).astype(int)

    max_radius = int(radii.max())
    median_intensity = []

    for r in range(max_radius + 1):
        mask = (radii == r)
        if np.any(mask):
            median_intensity.append(np.median(image[mask]))
        else:
            median_intensity.append(0)

    r_values = np.arange(max_radius + 1)
    params, _ = curve_fit(_polynomial_3rd_degree, r_values, median_intensity)
    intensity_profile = _polynomial_3rd_degree(r_values, *params)

    corrected_image = np.zeros_like(image)
    for r in range(max_radius + 1):
        mask = (radii == r)
        if intensity_profile[r] != 0:
            corrected_image[mask] = image[mask] / intensity_profile[r]

    if show_plot:
        plt.imshow(corrected_image, cmap='gray')
        plt.title("Limb Darkening Corrected Image")
        plt.colorbar()
        plt.show()

    return corrected_image
