"""
Bradley-Roth Adaptive Thresholding Module.

Implements the Bradley-Roth algorithm for adaptive image thresholding,
specifically designed for sunspot detection in solar images.

Reference:
    D. Bradley & G. Roth (2007). Adaptive Thresholding using the Integral Image.
    Journal of Graphics Tools, Vol. 12, No. 2, pp. 13-21.
"""

import numpy as np
import cv2
from typing import Tuple, Optional


def bradley_roth_threshold(
    image: np.ndarray,
    block_size: int = 50,
    constant: float = 10.0,
    convert_grayscale: bool = True,
) -> np.ndarray:
    """
    Apply Bradley-Roth adaptive thresholding to an image.
    
    The Bradley-Roth algorithm compares each pixel to the mean of a rectangular
    neighborhood. This is efficient for detecting sunspots in solar images as it
    adapts to local lighting conditions.

    Parameters
    ----------
    image : np.ndarray
        Input image (can be grayscale or color).
    block_size : int, optional
        Size of the neighborhood region (must be odd). Default is 50.
    constant : float, optional
        Constant subtracted from the mean. Values are in the range [-255, 255].
        Positive values typically work best. Default is 10.0.
    convert_grayscale : bool, optional
        If True and image is color, convert to grayscale first. Default is True.

    Returns
    -------
    np.ndarray
        Binary thresholded image (uint8, values 0 or 255).

    Raises
    ------
    ValueError
        If block_size is even or less than 3.
    """
    if block_size % 2 == 0 or block_size < 3:
        raise ValueError("block_size must be odd and >= 3")

    # Convert to grayscale if needed
    if len(image.shape) == 3 and convert_grayscale:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy() if len(image.shape) == 2 else image

    # Ensure image is float for processing
    img_float = gray.astype(np.float32)

    # Compute integral image
    integral = cv2.integral(img_float)

    # Compute mean using integral image
    height, width = gray.shape
    half_block = block_size // 2

    # Initialize output
    result = np.zeros_like(gray)

    for y in range(height):
        for x in range(width):
            # Define region boundaries
            x1 = max(0, x - half_block)
            y1 = max(0, y - half_block)
            x2 = min(width - 1, x + half_block)
            y2 = min(height - 1, y + half_block)

            # Calculate region size
            region_width = x2 - x1 + 1
            region_height = y2 - y1 + 1
            region_size = region_width * region_height

            # Get sum using integral image
            sum_val = (
                integral[y2 + 1, x2 + 1]
                - integral[y1, x2 + 1]
                - integral[y2 + 1, x1]
                + integral[y1, x1]
            )

            # Calculate mean
            mean_val = sum_val / region_size

            # Apply threshold
            if img_float[y, x] > (mean_val - constant):
                result[y, x] = 255
            else:
                result[y, x] = 0

    return result.astype(np.uint8)


def adaptive_threshold(
    image: np.ndarray,
    method: str = "bradley",
    block_size: int = 50,
    constant: float = 10.0,
    **kwargs
) -> np.ndarray:
    """
    Apply adaptive thresholding using various methods.

    Parameters
    ----------
    image : np.ndarray
        Input image.
    method : str, optional
        Thresholding method: 'bradley', 'gaussian', or 'mean'. Default is 'bradley'.
    block_size : int, optional
        Size of the neighborhood. Default is 50.
    constant : float, optional
        Constant to subtract from mean. Default is 10.0.
    **kwargs
        Additional arguments passed to the underlying method.

    Returns
    -------
    np.ndarray
        Binary thresholded image.
    """
    if method.lower() == "bradley":
        return bradley_roth_threshold(image, block_size, constant)
    elif method.lower() == "gaussian":
        return cv2.adaptiveThreshold(
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            block_size,
        )
    elif method.lower() == "mean":
        return cv2.adaptiveThreshold(
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            block_size,
        )
    else:
        raise ValueError(f"Unknown method: {method}")
