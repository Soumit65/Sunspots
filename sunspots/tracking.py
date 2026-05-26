"""
Sunspot tracking and display utilities.

Wraps astrolab's im.find_star for centroid finding, and provides the
display/process pipeline from the internship notebooks.
"""

import numpy as np
import matplotlib.pyplot as plt
from astrolab import imaging as im
from .thresholding import mask_sun

# Solar disk radius in pixels (DSLR images from the internship)
R_SUN = 1516


def display_spot(array, fig=None, ax=None, cmap="Greys_r"):
    """
    Display a solar image with axes scaled to solar radii.

    Axes run from -R_SUN to +R_SUN on both dimensions, matching the
    coordinate system used throughout the notebooks.

    Parameters
    ----------
    array : np.ndarray
        2D image array.
    fig : matplotlib.figure.Figure, optional
        Existing figure to draw into. Created if None.
    ax : matplotlib.axes.Axes, optional
        Existing axes to draw into. Created if None.
    cmap : str, optional
        Colormap. Default is 'Greys_r'.
    """
    if fig is None or ax is None:
        fig, ax = plt.subplots()
    ax.imshow(
        array,
        cmap=cmap,
        origin='lower',
        extent=[-R_SUN, +R_SUN, -R_SUN, +R_SUN],
    )


def find_spot(array, spot_pos, search=100, print_log=False, fig=None, ax=None):
    """
    Locate a sunspot centroid using astrolab's im.find_star on the inverted image.

    Sunspots are dark, so the image is inverted before passing to find_star,
    which expects bright objects.

    Parameters
    ----------
    array : np.ndarray
        2D image array (cropped and masked solar image).
    spot_pos : list or tuple
        Approximate [x, y] position of the spot in solar-radius coordinates,
        e.g. [-900, -700].
    search : int, optional
        Search box half-width in pixels. Default is 100.
    print_log : bool, optional
        If True, display the image with the located spot marked. Default is False.
    fig : matplotlib.figure.Figure, optional
        Existing figure (used when print_log=True).
    ax : matplotlib.axes.Axes, optional
        Existing axes (used when print_log=True).

    Returns
    -------
    tuple
        (x, y) centroid position returned by im.find_star.
    """
    if print_log and (fig is None or ax is None):
        fig, ax = plt.subplots()

    inverted_array = np.max(array) - array
    this_spot = im.find_star(inverted_array, star_pos=spot_pos, search=search, print_log=False)

    if print_log:
        ax.imshow(
            array,
            cmap="Greys_r",
            origin='lower',
            extent=[-R_SUN, +R_SUN, -R_SUN, +R_SUN],
        )
        ax.scatter(1515, 1515)
        ax.scatter(this_spot[0], this_spot[1], facecolor='none', ec='r')

    return this_spot


def process(image, spot_pos, print_log=False, fig=None, ax=None):
    """
    Full single-image processing pipeline: mask/crop the sun, then find a spot.

    Parameters
    ----------
    image : np.ndarray
        Raw solar image loaded with im.load_image.
    spot_pos : list or tuple
        Approximate [x, y] spot position in solar-radius coordinates.
    print_log : bool, optional
        Pass-through to mask_sun and find_spot for debug display. Default is False.
    fig : matplotlib.figure.Figure, optional
        Existing figure for display.
    ax : matplotlib.axes.Axes, optional
        Existing axes for display.

    Returns
    -------
    tuple
        (cropped_image, spot_position) where cropped_image is the masked/cropped
        array and spot_position is the (x, y) centroid from find_spot.
    """
    if print_log and (fig is None or ax is None):
        fig, ax = plt.subplots()

    this_crop = mask_sun(image, print_log=False)
    this_spot = find_spot(this_crop, spot_pos=spot_pos, print_log=print_log, fig=fig, ax=ax)

    return this_crop, this_spot


def process_image_list(image_list, rough_spot_list, print_log=True):
    """
    Process a list of images, returning crops and spot positions for each.

    Parameters
    ----------
    image_list : list of np.ndarray
        Images loaded with im.load_image (and optionally filtered).
    rough_spot_list : list of list
        List of approximate [x, y] spot positions, one per image.
    print_log : bool, optional
        Display each crop with spot marked. Default is True.

    Returns
    -------
    crop_list : list of np.ndarray
    spot_list : np.ndarray
        Shape (N, 2) array of (x, y) centroids.

    Examples
    --------
    >>> from astrolab import imaging as im
    >>> from scipy import ndimage as scp
    >>> raw = im.load_image("DSC_1036.JPG")
    >>> filtered = scp.gaussian_filter(raw, sigma=0.5, radius=2)
    >>> crops, spots = process_image_list([filtered], [[-900, -700]])
    """
    crop_list = []
    spot_list = []
    for image, spot_pos in zip(image_list, rough_spot_list):
        this_crop, this_spot = process(image, spot_pos=spot_pos, print_log=print_log)
        crop_list.append(this_crop)
        spot_list.append(this_spot)

    return crop_list, np.array(spot_list)
