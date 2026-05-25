# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024

### Added

#### Core Features
- Bradley-Roth adaptive thresholding implementation
- Automatic sunspot detection using contour analysis
- Area calculation and property measurement
- Sunspot data class with comprehensive properties
  - Area, perimeter, circularity, aspect ratio
  - Centroid and bounding box calculation
  - Contour storage for further analysis

#### Image Processing Utilities
- Image loading and saving
- Intensity normalization (minmax, zscore, histogram)
- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Gaussian blur for noise reduction
- Image resizing with aspect ratio preservation

#### Documentation
- Comprehensive API reference
- Getting started guide
- Installation instructions
- In-depth tutorials
- 8+ practical examples
- Frequently asked questions
- Sphinx-based documentation

#### Deployment & CI/CD
- GitHub Actions workflow for automatic documentation building
- GitHub Pages integration for online documentation
- Modern pyproject.toml configuration
- MIT License
- Professional README with badges

#### Package Configuration
- setuptools configuration
- Development and documentation dependencies
- Type hints throughout codebase
- Docstrings in Google style
- Proper module exports

### Features

**Thresholding Module**
- Bradley-Roth adaptive thresholding (primary algorithm)
- Gaussian adaptive thresholding
- Mean adaptive thresholding
- Configurable block size and constant parameters

**Detection Module**
- Multi-method sunspot detection
- Property calculation (area, perimeter, circularity)
- Filtering by area and properties
- Batch contour analysis
- Statistics generation

**Utilities Module**
- Multiple file format support (jpg, png, etc.)
- Image normalization methods
- Contrast enhancement (CLAHE)
- Noise reduction
- Image resizing

**Documentation**
- Complete API reference
- Usage examples
- Parameter tuning guide
- Troubleshooting guide
- FAQ section

### Technical Details

- **Language**: Python 3.8+
- **License**: MIT
- **Dependencies**: numpy, opencv-python, matplotlib, scipy, scikit-image, pillow
- **Package Format**: Modern pyproject.toml based
- **Documentation**: Sphinx with RTD theme
- **Testing**: Ready for pytest integration
- **CI/CD**: GitHub Actions ready

### Known Limitations

- CPU-based processing (GPU support planned)
- Batch processing requires manual loops (parallelization coming)
- Only black/white (binary) thresholding output
- Sunspot tracking is manual (will add automatic tracking)

### Future Roadmap

- [ ] GPU acceleration with OpenCV CUDA
- [ ] Automatic sunspot tracking across frames
- [ ] Additional thresholding methods
- [ ] Web interface for easy access
- [ ] More comprehensive tutorials
- [ ] Integration with solar observation databases
- [ ] Real-time processing capabilities
- [ ] Extended filtering options
- [ ] Performance optimizations
- [ ] More edge cases testing

---

## Version History

- **0.1.0** (2024): Initial release
  - Core functionality complete
  - Full documentation
  - GitHub Pages integration
  - MIT License
