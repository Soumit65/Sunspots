"""
Sunspots: Sunspot tracking, detection, and area calculation.

A Python package for detecting and analyzing sunspots from solar images
using Bradley-Roth adaptive thresholding and contour analysis.
"""

"""
Sunspots: Solar image analysis toolkit.
Developed during the Astro Lab Summer Internship 2024.
"""

__version__ = "0.1.0"
__author__ = "Soumit Rao"
__email__ = "rsoumit51@gmail.com"
__license__ = "MIT"

from .thresholding import *
from .area import *
from .correction import *
from .tracking import *
from .suit import *
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
from .suit import (
    load_suit_fits,
    detect_solar_disk,
    find_solar_center_fast,
    radial_flatten,
    extract_uv_features,
    segment_uv_structures,
    detect_uv_structures,
    plot_suit_pipeline,
)
