"""
Bradley-Roth adaptive thresholding for sunspot detection.

Your original implementation from the internship notebooks, packaged as
importable functions. Uses the integral image (cumulative sum) approach
with a sliding window of size image_width // Nx.

Reference:
    Bradley, D. & Roth, G. (2007). Adaptive Thresholding using the
    Integral Image. Journal of Graphics Tools, 12(2), 13-21.
"""

import numpy as np
import matplotlib.pyplot as plt
from astrolab import imaging as im


def mask_sun(image_array, sun_threshold=50, print_log=False, crop=True):
    """
    Create a mask isolating the solar disk and optionally crop to it.

    Finds the bounding edges of the sun by thresholding and taking row/column
    means of the mask. Uses astrolab's im.crop to return the cropped image.

    Parameters
    ----------
    image_array : np.ndarray
        2D grayscale image array.
    sun_threshold : float, optional
        Pixel value below which a pixel is considered background (not sun).
        Default is 50.
    print_log : bool, optional
        If True, display histogram and bounding-box overlay. Default is False.
    crop : bool, optional
        If True (default), return the cropped image. If False, return the
        raw bounding box coordinates and mask for further use.

    Returns
    -------
    np.ndarray
        Cropped image (if crop=True), or tuple (left, right, top, bottom, mask).
    """
    mask = ~(image_array < sun_threshold)

    if print_log:
        plt.hist(image_array.flatten())
        plt.show()

    v = np.mean(mask, axis=0)   # vertical average across columns
    v1 = np.argwhere(v > 0)

    h = np.mean(mask, axis=1)   # horizontal average across rows
    h1 = np.argwhere(h > 0)

    left   = v1[0][0]
    right  = v1[-1][0]
    bottom = h1[0][0]
    top    = h1[-1][0]

    if print_log:
        im.display(mask * image_array, stretch='linear')
        plt.gca().axhline(h1[0],  color='firebrick')
        plt.gca().axvline(v1[0],  color='firebrick')
        plt.gca().axhline(h1[-1], color='firebrick')
        plt.gca().axvline(v1[-1], color='firebrick')
        print(left, right, top, bottom)

    if crop:
        image_array = mask * image_array
        return im.crop(image_array, left=left, right=right, top=top, bottom=bottom)
    else:
        return left, right, top, bottom, mask


def b_roth(image_main, threshold, Nx=100, print_log=True):
    """
    Bradley-Roth adaptive thresholding using the integral image.

    For each pixel, computes the local mean over a window of size
    (image_width // Nx) using a 2-D cumulative sum (integral image),
    then marks the pixel as foreground if its value exceeds
    (local_mean * (100 - threshold) / 100).

    Parameters
    ----------
    image_main : np.ndarray
        2D grayscale image array (e.g. from im.load_image or mask_sun).
    threshold : float
        Sensitivity parameter (0-100). Higher values detect more spots.
        Typical range used in the internship: 8-15.
    Nx : int, optional
        Window size divisor. Window = image_width // Nx. Default is 100.
    print_log : bool, optional
        If True, display the thresholded result with a title. Default is True.

    Returns
    -------
    np.ndarray
        Integer binary array (1 = foreground/spot, 0 = background), same
        shape as image_main.
    """
    image = np.array(image_main).astype(float)

    s = image.shape[1] // Nx   # sliding window size
    t = threshold

    # integral image via two cumulative sums
    int_image = np.cumsum(np.cumsum(image, axis=1), axis=0)
    rows, cols = int_image.shape[:2]

    x, y = np.meshgrid(np.arange(cols), np.arange(rows))
    x = x.ravel()
    y = y.ravel()

    x_1 = x - s // 2
    x_2 = x + s // 2
    y_1 = y - s // 2
    y_2 = y + s // 2

    # clamp to image boundaries
    x_1[x_1 < 0] = 0
    y_1[y_1 < 0] = 0
    x_2[x_2 >= cols] = cols - 1
    y_2[y_2 >= rows] = rows - 1

    count = (x_2 - x_1) * (y_2 - y_1)
    total = (
        int_image[y_2, x_2]
        - int_image[(y_1 - 1), x_2]
        - int_image[y_2, (x_1 - 1)]
        + int_image[(y_1 - 1), (x_1 - 1)]
    )

    result = np.ones(rows * cols, dtype=bool)
    result[image.ravel() * count <= total * (100 - t) / 100.0] = False

    result = np.reshape(result, (rows, cols)).astype(int)

    if print_log:
        plt.imshow(result, cmap='grey', origin='lower')
        plt.title(f'Bradley-Roth Image [Nx={Nx}, threshold={threshold}]')

    return result
