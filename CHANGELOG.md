# Changelog

All notable changes to SuryaPy are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024

### Added

#### Core Thresholding
- `b_roth()` — Bradley-Roth adaptive thresholding using integral images (O(1) window queries)
- `mask_sun()` — Solar disk masking and cropping using astrolab

#### Sunspot Tracking
- `find_spot()` — Centroid locating via astrolab's `find_star` on inverted image
- `process()` — Single-image pipeline: mask → find spot
- `process_image_list()` — Batch processing of multiple images
- `display_spot()` — Solar-coordinate image display helper

#### Corrections & Analysis
- `limb_darkening_correction()` — Radial median profile + 3rd-degree polynomial fit
- `find_components()` — Morphological cleanup + connected component labeling + size filtering
- `inspect_component()` — Detailed inspection of a single labeled component

#### Physical Conversions
- `foreshortening_correction()` — Project area from image plane to solar surface
- `pixels_to_km2()` — Pixel-to-kilometer conversion
- `km2_to_millionths()` — km² to millionths of solar hemisphere (MH)
- `angular_distance()` — Angular position on the solar disk

#### Documentation
- Complete API reference with function signatures and examples
- Getting started guide with workflow overview
- Quick start (5-minute intro)
- Installation instructions
- 5 in-depth tutorials (Bradley-Roth, limb darkening, connected components, foreshortening, units)
- 7 practical examples from internship notebooks
- Comprehensive FAQ with 30+ Q&A

#### Packaging & Deployment
- Modern `pyproject.toml` configuration (PEP 517/518)
- MIT License
- GitHub Actions workflow for auto-deploying docs to GitHub Pages
- Sphinx documentation with RTD theme
- Professional README with feature list and examples

### Technical Stack

- **Language**: Python 3.8+
- **Core**: numpy, scipy (ndimage), matplotlib
- **Imaging**: astrolab (your college's solar library)
- **Docs**: Sphinx + sphinx-rtd-theme
- **CI/CD**: GitHub Actions

### Features Highlight

✨ **Bradley-Roth Adaptive Thresholding** — Integral-image based for sunspot detection

🎯 **Connected Component Analysis** — Morphological cleanup + scipy.ndimage.label for individual sunspot identification

🔬 **Physical Corrections** — Foreshortening angle correction, limb darkening removal

📍 **Spot Tracking** — Multi-image registration via astrolab's centroid finding

📊 **Standard Units** — Automatic conversion to millionths of solar hemisphere (MH)

### Known Limitations

- CPU-based processing (GPU support may come in future)
- Manual spot tracking across frames (auto-tracking planned)
- Requires astrolab (your college's library)

### Future Roadmap

- [ ] Automatic sunspot tracking across image sequences
- [ ] Performance profiling and optimization
- [ ] More extensive unit test suite
- [ ] Support for different solar disk projections
- [ ] Integration with NOAA/SIDC databases
- [ ] Web interface for easy access
- [ ] GPU acceleration (CUDA)

### Acknowledgments

Developed during the **2024 Summer Astronomy Internship**. Uses:
- Bradley-Roth algorithm from Bradley & Roth (2007)
- Astrolab (your college's solar imaging library)
- Scipy's connected component analysis
- Foreshortening correction from solar physics literature

### Citation

If you use SuryaPy in research:

```bibtex
@software{suryapy2024,
  author = {Dey, Soumit},
  title = {SuryaPy: Solar Sunspot Detection and Analysis},
  year = {2024},
  url = {https://github.com/Soumit65/SuryaPy}
}
```

---

## Version History

- **0.1.0** (2024) — Initial release. Core functionality from internship notebooks packaged and documented.
