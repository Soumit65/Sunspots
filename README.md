# SuryaPy ☀️

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![GitHub](https://img.shields.io/badge/GitHub-Soumit65%2FSuryaPy-blue?logo=github)](https://github.com/Soumit65/SuryaPy)

**SuryaPy** — from *Surya*, the Sun in Sanskrit — is a Python package for detecting, analyzing, and measuring sunspots from solar observations. Built on my (Soumit Rao) 2024 summer astronomy internship work at Ashoka University.

Uses the **Bradley-Roth adaptive thresholding algorithm** with **connected component analysis** to identify sunspots, applies physical corrections (foreshortening, limb darkening), and converts measurements to standard solar physics units.

## Features

**Bradley-Roth Adaptive Thresholding** — Integral-image based local contrast detection, robust to varying lighting

**Connected Component Analysis** — Morphological cleanup + `scipy.ndimage.label` for automatic sunspot identification

**Physical Corrections** — Foreshortening correction, limb darkening removal, pixel-to-km² conversion

**Spot Tracking** — Integration with `astrolab`'s centroid-finding for multi-image registration

**Standard Units** — Convert to millionths of solar hemisphere (MH), angular distances, and heliocentric coordinates

**Built on Astrolab** — Leverages Astrolab package by Philip Cherian - https://astrolab.readthedocs.io/en/latest/

## Quick Start

```python
from astrolab import imaging as im
from scipy import ndimage as scp
import suryapy

# Load and filter a solar image
raw_image = im.load_image("DSC_1036.JPG")
filtered = scp.gaussian_filter(raw_image, sigma=0.5, radius=2)

# Mask the solar disk and crop
cropped = suryapy.mask_sun(filtered, sun_threshold=50)

# Apply Bradley-Roth thresholding
br_mask = suryapy.b_roth(cropped, threshold=9, Nx=100)

# Find connected components (sunspots)
labeled, n_comp, large_mask, sizes, bbox = suryapy.find_components(
    br_mask, cropped, min_size=1000
)

# Correct for foreshortening at position (y, z)
corrected_area_px = suryapy.foreshortening_correction(
    area_pixels=1276, y=-700, z=-900, R_sun=1511
)

# Convert to physical units
area_km2 = suryapy.pixels_to_km2(corrected_area_px, km_per_pixel=458.58)
area_mh = suryapy.km2_to_millionths(area_km2)

print(f"Sunspot area: {area_mh:.2f} MH")
```

## Installation

### From Source (Recommended)

```bash
git clone https://github.com/Soumit65/SuryaPy.git
cd SuryaPy
pip install -e .
```

### With Development Tools

```bash
pip install -e ".[dev,docs,jupyter]"
```

### From PyPI (Coming Soon)

```bash
pip install suryapy
```

## Documentation

Full documentation with tutorials and examples: **https://soumit65.github.io/SuryaPy/**

- **Getting Started** — Workflow and core concepts
- **API Reference** — All functions documented
- **Tutorials** — Bradley-Roth algorithm, limb darkening, connected components
- **Examples** — 6+ complete working examples
- **FAQ** — Common questions and troubleshooting

## Package Structure

```
sunspots/
├── __init__.py           # Package exports
├── thresholding.py       # b_roth, mask_sun
├── tracking.py           # find_spot, process, display_spot
├── correction.py         # limb_darkening_correction
└── area.py              # Connected components, foreshortening, unit conversion
```

## Core Functions

### Thresholding

```python
# Bradley-Roth adaptive thresholding (your internship algorithm)
br_mask = suryapy.b_roth(image, threshold=9, Nx=100, print_log=True)

# Mask and crop the solar disk
cropped = suryapy.mask_sun(image, sun_threshold=50, crop=True)
```

### Tracking & Alignment

```python
# Find a sunspot centroid (uses astrolab's find_star internally)
spot_pos = suryapy.find_spot(cropped, spot_pos=[-900, -700], search=100)

# Full processing pipeline: crop → find spot
cropped, spot_centroid = suryapy.process(
    image, spot_pos=[-900, -700], print_log=True
)

# Process multiple images at once
crops, spots = suryapy.process_image_list(
    [image1, image2, image3],
    [[-900, -700], [-250, 500], [220, 450]]
)
```

### Corrections & Analysis

```python
# Remove limb darkening via radial median profile
corrected = suryapy.limb_darkening_correction(cropped, show_plot=True)

# Connected component analysis with morphological cleanup
labeled, n, large_mask, sizes, bbox = suryapy.find_components(
    br_mask, cropped, min_size=1000, print_log=True
)

# Inspect a single component
info = suryapy.inspect_component(
    target_label=77, labeled_image=labeled, num_components=n,
    bound_box=bbox, br_mask=br_mask, image=cropped
)
```

### Physical Conversions

```python
# Correct for foreshortening (projection angle)
area_corrected = suryapy.foreshortening_correction(
    area_pixels=1276, y=-700, z=-900, R_sun=1511
)

# Pixel → km²
area_km2 = suryapy.pixels_to_km2(area_corrected, km_per_pixel=458.58)

# km² → millionths of solar hemisphere (standard solar physics unit)
area_mh = suryapy.km2_to_millionths(area_km2)

# Angular distance from disk center
ang_dist = suryapy.angular_distance(x_spot=0, y_spot=1000, pixel_radius=1516)
```

## Parameters Reference

### Bradley-Roth Thresholding

| Parameter | Default | Effect |
|-----------|---------|--------|
| `threshold` | 9 | Sensitivity (5-20 typical). Higher = more aggressive detection |
| `Nx` | 100 | Window divisor. Larger window if Nx is smaller |

### Connected Components

| Parameter | Default | Effect |
|-----------|---------|--------|
| `min_size` | 1000 | Minimum component area (pixels) to keep |

### Calibration (DSLR + SIDC Example)

| Instrument | km/pixel | pixels² → MH |
|------------|----------|----------|
| DSLR (internship) | 458.58 | multiply by `(458.58/696000)² × 1e6` |
| SIDC | 738.44 | multiply by `(738.44/696000)² × 1e6` |

## Example Notebook Workflow

Replicating the notebook analysis from your internship:

```python
from astrolab import imaging as im
from scipy import ndimage as scp
import matplotlib.pyplot as plt
import suryapy as sio  # your alias

# 1. Load and preprocess
raw = im.load_image("DSC_1036.JPG")
filtered = scp.gaussian_filter(raw, sigma=0.5, radius=2)

# 2. Mask and crop
cropped = sio.mask_sun(filtered, sun_threshold=50)

# 3. Apply corrections
corrected = sio.limb_darkening_correction(cropped)

# 4. Threshold
br = sio.b_roth(cropped, threshold=9, Nx=100)

# 5. Morphological cleanup
from scipy.ndimage import binary_opening, binary_closing
struct = np.ones((3, 3))
opened = binary_opening(cropped, structure=struct)
closed = binary_closing(br, structure=struct)
isolated = closed * cropped * opened

# 6. Find components
labeled, n, large, sizes, bbox = sio.find_components(
    br, cropped, min_size=1000
)

# 7. Measure and correct
component_info = sio.inspect_component(1, labeled, n, bbox, br, cropped)
area_px = component_info['area_pixels']
area_corr = sio.foreshortening_correction(area_px, y=-700, z=-900)
area_mh = sio.km2_to_millionths(sio.pixels_to_km2(area_corr, 458.58))

print(f"Sunspot area: {area_mh:.2f} MH")
```

## Dependencies

- **astrolab** ≥ 0.1.0 — solar imaging library (your college's work!)
- **numpy** ≥ 1.19.0 — array operations
- **scipy** ≥ 1.5.0 — ndimage, optimize
- **matplotlib** ≥ 3.3.0 — plotting

No OpenCV — pure numpy/scipy implementation of Bradley-Roth.

## Requirements

- Python 3.8+
- astrolab properly installed and configured

## Contributing

Contributions welcome! Fork, branch, commit, and PR.

```bash
git checkout -b feature/cool-feature
# ... make changes ...
git commit -m "Add cool feature"
git push origin feature/cool-feature
```

## Citation

If you use SuryaPy in your research:

```bibtex
@software{suryapy2024,
  author = {Rao, Soumit},
  title = {SuryaPy: Solar Sunspot Detection and Analysis},
  year = {2024},
  url = {https://github.com/Soumit65/SuryaPy}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- Developed as part of the 2024 Summer Astronomy Internship
- Uses [astrolab](https://github.com/your-college/astrolab) — the solar imaging library from your college
- Bradley-Roth algorithm: Bradley & Roth (2007), *Journal of Graphics Tools*
- Connected component analysis via scipy.ndimage

## References

1. Bradley, D., & Roth, G. (2007). Adaptive Thresholding using the Integral Image. *Journal of Graphics Tools*, 12(2), 13-21.
2. Foreshortening correction formulas from solar physics literature
3. SIDC/NOAA standards for sunspot area measurement in millionths of hemisphere

## Contact

- **GitHub**: [@Soumit65](https://github.com/Soumit65)
- **Issues**: [GitHub Issues](https://github.com/Soumit65/SuryaPy/issues)
- **Docs**: [https://soumit65.github.io/SuryaPy/](https://soumit65.github.io/SuryaPy/)

---

**Let's observe the sun. 🌞**
