"""
Sunspot Area Calculation Module.

Functions for detecting sunspots, calculating their areas, and analyzing
their properties from binary or grayscale images.
"""

import numpy as np
import cv2
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Sunspot:
    """Data class representing a detected sunspot."""

    area: float
    perimeter: float
    centroid: Tuple[float, float]
    bounding_box: Tuple[int, int, int, int]
    contour: np.ndarray
    circularity: float
    aspect_ratio: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "area": self.area,
            "perimeter": self.perimeter,
            "centroid": self.centroid,
            "bounding_box": self.bounding_box,
            "circularity": self.circularity,
            "aspect_ratio": self.aspect_ratio,
        }


def detect_sunspots(
    image: np.ndarray,
    min_area: float = 50.0,
    max_area: Optional[float] = None,
    threshold_method: str = "otsu",
) -> List[Sunspot]:
    """
    Detect sunspots in a solar image.

    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or color).
    min_area : float, optional
        Minimum area threshold for sunspot detection. Default is 50.0.
    max_area : float, optional
        Maximum area threshold for sunspot detection. Default is None (no limit).
    threshold_method : str, optional
        Thresholding method: 'otsu' or 'binary'. Default is 'otsu'.

    Returns
    -------
    List[Sunspot]
        List of detected sunspots with their properties.
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Apply thresholding
    if threshold_method.lower() == "otsu":
        _, binary = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
    else:
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    sunspots = []

    for contour in contours:
        # Calculate area
        area = cv2.contourArea(contour)

        # Filter by area
        if area < min_area:
            continue
        if max_area is not None and area > max_area:
            continue

        # Calculate properties
        perimeter = cv2.arcLength(contour, True)
        moments = cv2.moments(contour)

        # Calculate centroid
        if moments["m00"] > 0:
            cx = moments["m10"] / moments["m00"]
            cy = moments["m01"] / moments["m00"]
        else:
            continue

        # Bounding box
        x, y, w, h = cv2.boundingRect(contour)

        # Circularity (4π * area / perimeter²)
        if perimeter > 0:
            circularity = (4 * np.pi * area) / (perimeter ** 2)
        else:
            circularity = 0.0

        # Aspect ratio
        aspect_ratio = float(w) / float(h) if h > 0 else 1.0

        sunspot = Sunspot(
            area=area,
            perimeter=perimeter,
            centroid=(cx, cy),
            bounding_box=(x, y, w, h),
            contour=contour,
            circularity=circularity,
            aspect_ratio=aspect_ratio,
        )

        sunspots.append(sunspot)

    return sunspots


def calculate_area(
    binary_image: np.ndarray,
    pixel_to_mm: float = 1.0,
) -> float:
    """
    Calculate total area of all white regions in a binary image.

    Parameters
    ----------
    binary_image : np.ndarray
        Binary image (values 0 or 255).
    pixel_to_mm : float, optional
        Conversion factor from pixels to real-world units. Default is 1.0.

    Returns
    -------
    float
        Total area in specified units.
    """
    # Count white pixels
    white_pixels = np.sum(binary_image > 127)
    area = white_pixels * (pixel_to_mm ** 2)
    return area


def analyze_contours(
    image: np.ndarray,
    min_area: float = 50.0,
    max_area: Optional[float] = None,
) -> Tuple[List[Sunspot], Dict[str, Any]]:
    """
    Analyze contours in a binary image and return statistics.

    Parameters
    ----------
    image : np.ndarray
        Binary input image.
    min_area : float, optional
        Minimum area filter. Default is 50.0.
    max_area : float, optional
        Maximum area filter. Default is None.

    Returns
    -------
    Tuple[List[Sunspot], Dict[str, Any]]
        Tuple of (list of detected sunspots, statistics dictionary).
    """
    sunspots = detect_sunspots(image, min_area, max_area)

    # Calculate statistics
    if len(sunspots) > 0:
        areas = [s.area for s in sunspots]
        circularities = [s.circularity for s in sunspots]

        stats = {
            "count": len(sunspots),
            "total_area": sum(areas),
            "mean_area": np.mean(areas),
            "std_area": np.std(areas),
            "min_area": min(areas),
            "max_area": max(areas),
            "mean_circularity": np.mean(circularities),
            "mean_aspect_ratio": np.mean([s.aspect_ratio for s in sunspots]),
        }
    else:
        stats = {
            "count": 0,
            "total_area": 0.0,
            "mean_area": 0.0,
            "std_area": 0.0,
            "min_area": 0.0,
            "max_area": 0.0,
            "mean_circularity": 0.0,
            "mean_aspect_ratio": 0.0,
        }

    return sunspots, stats


def draw_sunspots(
    image: np.ndarray,
    sunspots: List[Sunspot],
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2,
) -> np.ndarray:
    """
    Draw detected sunspots on an image.

    Parameters
    ----------
    image : np.ndarray
        Input image.
    sunspots : List[Sunspot]
        List of detected sunspots.
    color : Tuple[int, int, int], optional
        BGR color for drawing. Default is green (0, 255, 0).
    thickness : int, optional
        Line thickness. Default is 2.

    Returns
    -------
    np.ndarray
        Image with drawn sunspots.
    """
    result = image.copy()

    for sunspot in sunspots:
        # Draw contour
        cv2.drawContours(result, [sunspot.contour], 0, color, thickness)

        # Draw centroid
        cx, cy = sunspot.centroid
        cv2.circle(result, (int(cx), int(cy)), 5, color, -1)

    return result
