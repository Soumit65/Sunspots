"""
Sunspot area calculation using connected component analysis.

Implements the scipy.ndimage connected-component pipeline from the
internship notebook:
  1. Morphological open/close to clean the Bradley-Roth mask
  2. scp.label to find connected components
  3. Size filtering by min_size threshold
  4. Foreshortening (projection) correction
  5. Physical area conversion (pixels → km² → millionths of hemisphere)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as scp
from astrolab import imaging as im


# ---------------------------------------------------------------------------
# Connected component analysis
# ---------------------------------------------------------------------------

def find_components(br_mask, image, min_size=1000, print_log=True):
    """
    Apply morphological cleanup, label connected components, and filter by size.

    Replicates the notebook workflow:
      - binary_opening on the raw image (removes small bright noise)
      - binary_closing on the Bradley-Roth mask (fills gaps in spots)
      - multiply to isolate sunspot regions
      - scp.label on zero-valued pixels (sunspots are dark → value 0)
      - filter out components smaller than min_size

    Parameters
    ----------
    br_mask : np.ndarray
        Binary mask from b_roth (1 = bright background, 0 = dark spot).
    image : np.ndarray
        The corresponding cropped solar image (same shape as br_mask).
    min_size : int, optional
        Minimum component area in pixels to keep. Default is 1000.
    print_log : bool, optional
        If True, display the filtered components image. Default is True.

    Returns
    -------
    labeled_image : np.ndarray
        Integer array where each connected component has a unique label.
    num_components : int
        Total number of components found (before size filtering).
    large_components_mask : np.ndarray
        Boolean mask of only the components >= min_size.
    component_sizes : np.ndarray
        Area in pixels for every component (index i → label i+1).
    bound_box : list
        Bounding slices from scp.find_objects, one per component.
    """
    structuring_element = np.ones((3, 3))

    opened_mask   = scp.binary_opening(image,   structure=structuring_element)
    closed_spots  = scp.binary_closing(br_mask, structure=structuring_element)
    isolated_sunspots = closed_spots * image * opened_mask

    # sunspots are 0-valued after the mask, so label the zeros
    labeled_image, num_components = scp.label(isolated_sunspots == 0)

    component_sizes = np.bincount(labeled_image.ravel())[1:]  # skip background label 0
    bound_box = scp.find_objects(labeled_image)

    large_components = component_sizes >= min_size
    large_components_mask = np.isin(
        labeled_image, np.nonzero(large_components)[0] + 1
    )

    if print_log:
        for i, size in enumerate(component_sizes):
            if size >= min_size:
                print(f"Component {i + 1}: Area = {size} pixels")

        plt.figure(figsize=(10, 10))
        plt.imshow(large_components_mask, cmap='Greys_r')
        plt.title(f"Filtered Components (min size: {min_size} pixels)")
        plt.show()

    return labeled_image, num_components, large_components_mask, component_sizes, bound_box


def inspect_component(target_label, labeled_image, num_components, bound_box,
                       br_mask, image, print_log=True):
    """
    Display and return information about a single labelled component.

    Parameters
    ----------
    target_label : int
        The component label to inspect (1-based, matching scp.label output).
    labeled_image : np.ndarray
        Output of scp.label.
    num_components : int
        Total component count (for bounds checking).
    bound_box : list
        Output of scp.find_objects.
    br_mask : np.ndarray
        The Bradley-Roth mask (for comparison display).
    image : np.ndarray
        The cropped solar image.
    print_log : bool, optional
        Display the component and comparison. Default is True.

    Returns
    -------
    dict with keys: label, y_start, y_end, x_start, x_end, height, width, area_pixels
    """
    if target_label > num_components:
        print(f"Label {target_label} exceeds total components: {num_components}")
        return None

    target_slice = bound_box[target_label - 1]
    if not target_slice:
        print(f"No component found with label {target_label}")
        return None

    y_slice, x_slice = target_slice
    y_start, y_end = y_slice.start, y_slice.stop
    x_start, x_end = x_slice.start, x_slice.stop
    height = y_end - y_start
    width  = x_end - x_start

    component_mask = np.zeros_like(labeled_image)
    component_mask[y_slice, x_slice] = (labeled_image[y_slice, x_slice] == target_label)
    area_pixels = int(component_mask.sum())

    print(f"Component {target_label}: "
          f"y=[{y_start}, {y_end}], x=[{x_start}, {x_end}], "
          f"Height={height} px, Width={width} px, Area={area_pixels} px")

    if print_log:
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 10))
        im.display(component_mask * image, fig=fig, ax=axes[1], cmap='inferno')
        im.display(br_mask * image,        fig=fig, ax=axes[0], cmap='inferno')
        plt.suptitle(f"Component {target_label} Highlighted")
        plt.show()

    return dict(
        label=target_label,
        y_start=y_start, y_end=y_end,
        x_start=x_start, x_end=x_end,
        height=height, width=width,
        area_pixels=area_pixels,
    )


# ---------------------------------------------------------------------------
# Foreshortening correction
# ---------------------------------------------------------------------------

def foreshortening_correction(area_pixels, y, z, R_sun=1511):
    """
    Correct sunspot area for foreshortening (projection onto the solar sphere).

    Uses the formula derived in the notebook:
        A_corrected = A_image / sqrt(1 - (y/R)^2 - (z/R)^2)

    where y, z are the heliocentric coordinates of the spot centre in pixels
    and R is the solar radius in pixels.

    Parameters
    ----------
    area_pixels : float
        Observed area in image pixels.
    y : float
        y-coordinate of the spot centre in pixels (from image centre).
    z : float
        z-coordinate of the spot centre in pixels (from image centre).
    R_sun : float, optional
        Solar disk radius in pixels. Default is 1511 (from notebook).

    Returns
    -------
    float
        Corrected area in pixels.

    Examples
    --------
    >>> corrected = foreshortening_correction(1276, y=-700, z=-900, R_sun=1511)
    """
    return area_pixels / np.sqrt(1 - (y / R_sun)**2 - (z / R_sun)**2)


# ---------------------------------------------------------------------------
# Physical area conversion
# ---------------------------------------------------------------------------

def pixels_to_km2(area_pixels, km_per_pixel):
    """
    Convert an area in pixels to km².

    Parameters
    ----------
    area_pixels : float
        Area in pixels (corrected or uncorrected).
    km_per_pixel : float
        Scale: km per pixel for your instrument.
        From the notebook: DSLR ≈ 458.58 km/px, SIDC ≈ 738.44 km/px.

    Returns
    -------
    float
        Area in km².
    """
    return area_pixels * km_per_pixel**2


def km2_to_millionths(area_km2, R_sun_km=696_000):
    """
    Convert km² to millionths of the solar hemisphere (MH), the standard
    unit for sunspot area in solar physics.

    MH = (area_km2 / (2 * pi * R_sun_km^2)) * 1e6

    Parameters
    ----------
    area_km2 : float
        Area in km².
    R_sun_km : float, optional
        Solar radius in km. Default is 696,000 km.

    Returns
    -------
    float
        Area in millionths of solar hemisphere.
    """
    hemisphere_km2 = 2 * np.pi * R_sun_km**2
    return (area_km2 / hemisphere_km2) * 1e6


def angular_distance(x_spot, y_spot, pixel_radius=1516,
                     angular_radius_deg=0.27, x_center=0, y_center=0):
    """
    Compute the angular distance of a spot from the solar disc centre.

    Converts pixel distance to angular distance using the known angular
    radius of the sun and the pixel radius of the disc.

    Parameters
    ----------
    x_spot : float
        x-coordinate of the spot (in solar-radius pixel coords).
    y_spot : float
        y-coordinate of the spot.
    pixel_radius : float, optional
        Solar disc radius in pixels. Default is 1516.
    angular_radius_deg : float, optional
        Angular radius of the sun in degrees. Default is 0.27 (half of 0.53°).
    x_center : float, optional
        x-coordinate of disc centre. Default is 0.
    y_center : float, optional
        y-coordinate of disc centre. Default is 0.

    Returns
    -------
    float
        Angular distance in degrees.
    """
    d_pixels = np.sqrt((x_spot - x_center)**2 + (y_spot - y_center)**2)
    angular_distance_per_pixel = angular_radius_deg / pixel_radius
    return d_pixels * angular_distance_per_pixel
