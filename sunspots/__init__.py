"""
Sunspots: Sunspot tracking, detection, and area calculation.

A Python package for detecting and analyzing sunspots from solar images
using Bradley-Roth adaptive thresholding and contour analysis.
"""

__version__ = "0.1.0"
__author__ = "Soumit Rao"
__email__ = "rsoumit51@gmail.com"
__license__ = "MIT"

from .thresholding import bradley_roth_threshold, adaptive_threshold
from .area_calculator import calculate_area, analyze_contours, detect_sunspots
from .utils import load_image, save_image, normalize_image

__all__ = [
    "bradley_roth_threshold",
    "adaptive_threshold",
    "calculate_area",
    "analyze_contours",
    "detect_sunspots",
    "load_image",
    "save_image",
    "normalize_image",
]
