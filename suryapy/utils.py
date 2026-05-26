"""
Utility functions for image processing and I/O operations.
"""

import cv2
import numpy as np
from typing import Optional, Tuple


def load_image(
    path: str,
    as_grayscale: bool = False,
) -> np.ndarray:
    """
    Load an image from disk.

    Parameters
    ----------
    path : str
        Path to the image file.
    as_grayscale : bool, optional
        If True, load as grayscale. Default is False.

    Returns
    -------
    np.ndarray
        Loaded image array.

    Raises
    ------
    FileNotFoundError
        If the image file does not exist.
    """
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {path}")

    if as_grayscale:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image


def save_image(
    path: str,
    image: np.ndarray,
) -> bool:
    """
    Save an image to disk.

    Parameters
    ----------
    path : str
        Output file path.
    image : np.ndarray
        Image array to save.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    return cv2.imwrite(path, image)


def normalize_image(
    image: np.ndarray,
    method: str = "minmax",
) -> np.ndarray:
    """
    Normalize image intensity values.

    Parameters
    ----------
    image : np.ndarray
        Input image.
    method : str, optional
        Normalization method: 'minmax', 'zscore', or 'histogram'. Default is 'minmax'.

    Returns
    -------
    np.ndarray
        Normalized image.
    """
    if method == "minmax":
        min_val = image.min()
        max_val = image.max()
        if max_val - min_val > 0:
            return ((image - min_val) / (max_val - min_val) * 255).astype(np.uint8)
        return image.astype(np.uint8)

    elif method == "zscore":
        mean = image.mean()
        std = image.std()
        if std > 0:
            normalized = ((image - mean) / std)
            normalized = np.clip(normalized * 127 + 127, 0, 255)
            return normalized.astype(np.uint8)
        return image.astype(np.uint8)

    elif method == "histogram":
        return cv2.equalizeHist(image.astype(np.uint8))

    else:
        raise ValueError(f"Unknown normalization method: {method}")


def resize_image(
    image: np.ndarray,
    width: Optional[int] = None,
    height: Optional[int] = None,
    scale: Optional[float] = None,
) -> np.ndarray:
    """
    Resize an image while maintaining aspect ratio.

    Parameters
    ----------
    image : np.ndarray
        Input image.
    width : int, optional
        Target width.
    height : int, optional
        Target height.
    scale : float, optional
        Scale factor (0-1).

    Returns
    -------
    np.ndarray
        Resized image.
    """
    h, w = image.shape[:2]

    if scale is not None:
        new_width = int(w * scale)
        new_height = int(h * scale)
    elif width is not None and height is None:
        scale_factor = width / w
        new_width = width
        new_height = int(h * scale_factor)
    elif height is not None and width is None:
        scale_factor = height / h
        new_height = height
        new_width = int(w * scale_factor)
    elif width is not None and height is not None:
        new_width = width
        new_height = height
    else:
        return image

    return cv2.resize(image, (new_width, new_height))


def apply_clahe(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_size: int = 8,
) -> np.ndarray:
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE).

    Parameters
    ----------
    image : np.ndarray
        Input image.
    clip_limit : float, optional
        Contrast limit. Default is 2.0.
    tile_size : int, optional
        Tile size. Default is 8.

    Returns
    -------
    np.ndarray
        Enhanced image.
    """
    if len(image.shape) == 3:
        # Convert to LAB color space, apply CLAHE to L channel
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
        l = clahe.apply(l)

        enhanced = cv2.merge([l, a, b])
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
        return clahe.apply(image)


def gaussian_blur(
    image: np.ndarray,
    kernel_size: int = 5,
    sigma: float = 1.0,
) -> np.ndarray:
    """
    Apply Gaussian blur to reduce noise.

    Parameters
    ----------
    image : np.ndarray
        Input image.
    kernel_size : int, optional
        Kernel size (must be odd). Default is 5.
    sigma : float, optional
        Standard deviation. Default is 1.0.

    Returns
    -------
    np.ndarray
        Blurred image.
    """
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
