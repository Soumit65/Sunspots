"""
SuryaPy: Solar observation and sunspot analysis package.

A Python package built on your internship work for detecting and analyzing
sunspots from solar images using the Bradley-Roth adaptive thresholding
algorithm with connected component analysis and physical corrections.

Built with astrolab and scipy.
"""

__version__ = "0.1.0"
__author__ = "Soumit Dey"
__email__ = "your.email@example.com"
__license__ = "MIT"

# Thresholding
from .thresholding import b_roth, mask_sun

# Tracking
from .tracking import display_spot, find_spot, process, process_image_list

# Correction
from .correction import limb_darkening_correction

# Area calculation
from .area import (
    find_components,
    inspect_component,
    foreshortening_correction,
    pixels_to_km2,
    km2_to_millionths,
    angular_distance,
)

__all__ = [
    # Thresholding
    "b_roth",
    "mask_sun",
    # Tracking
    "display_spot",
    "find_spot",
    "process",
    "process_image_list",
    # Correction
    "limb_darkening_correction",
    # Area
    "find_components",
    "inspect_component",
    "foreshortening_correction",
    "pixels_to_km2",
    "km2_to_millionths",
    "angular_distance",
]
