# Sunspots

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![GitHub](https://img.shields.io/badge/GitHub-Soumit65%2FSunspots-blue?logo=github)](https://github.com/Soumit65/Sunspots)

A Python package for detecting, tracking, and analyzing sunspots from solar images using adaptive thresholding and contour analysis.

## Features

- **Bradley-Roth Adaptive Thresholding**: Efficient detection algorithm adapted for sunspot identification
- **Sunspot Detection**: Automatic detection of sunspots with contour analysis
- **Area Calculation**: Precise area measurement of detected sunspots
- **Property Analysis**: Calculate circularity, aspect ratio, centroid, and more
- **Multiple Thresholding Methods**: Support for Otsu, Gaussian, and Mean adaptive thresholding
- **Image Processing Utilities**: Loading, normalization, CLAHE enhancement, and more
- **Simple API**: Easy-to-use functions for both quick analysis and advanced workflows

## Installation

### From PyPI (Coming Soon)

```bash
pip install sunspots
```

### From Source

```bash
git clone https://github.com/Soumit65/Sunspots.git
cd Sunspots
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev,docs]"
```

## Quick Start

```python
import sunspots
from sunspots import detect_sunspots, load_image, draw_sunspots

# Load an image
image = sunspots.load_image("solar_image.jpg")

# Detect sunspots
detected_spots = sunspots.detect_sunspots(image, min_area=50)

# Draw results
result = sunspots.draw_sunspots(image, detected_spots)

# Print statistics
for i, spot in enumerate(detected_spots):
    print(f"Sunspot {i+1}:")
    print(f"  Area: {spot.area:.2f} pixels")
    print(f"  Circularity: {spot.circularity:.3f}")
    print(f"  Centroid: {spot.centroid}")
```

## Usage Examples

### Basic Thresholding

```python
from sunspots import bradley_roth_threshold, load_image, save_image

# Load image
image = load_image("solar_image.jpg")

# Apply Bradley-Roth adaptive thresholding
binary = bradley_roth_threshold(image, block_size=51, constant=10)

# Save result
save_image("thresholded.jpg", binary)
```

### Advanced Contour Analysis

```python
from sunspots import analyze_contours

# Analyze contours with statistics
sunspots_list, stats = analyze_contours(binary_image, min_area=50)

print(f"Number of sunspots: {stats['count']}")
print(f"Total area: {stats['total_area']:.2f}")
print(f"Mean area: {stats['mean_area']:.2f}")
print(f"Mean circularity: {stats['mean_circularity']:.3f}")
```

### Image Enhancement

```python
from sunspots import load_image, apply_clahe, gaussian_blur, normalize_image

image = load_image("solar_image.jpg")

# Apply preprocessing
enhanced = apply_clahe(image, clip_limit=2.0)
enhanced = gaussian_blur(enhanced, kernel_size=5)
normalized = normalize_image(enhanced, method="minmax")
```

## API Reference

### Core Functions

#### `bradley_roth_threshold(image, block_size=50, constant=10.0, convert_grayscale=True)`
Apply Bradley-Roth adaptive thresholding.

**Parameters:**
- `image` (np.ndarray): Input image
- `block_size` (int): Size of neighborhood (must be odd)
- `constant` (float): Constant subtracted from mean
- `convert_grayscale` (bool): Convert to grayscale if color

**Returns:** Binary image (uint8)

#### `detect_sunspots(image, min_area=50, max_area=None, threshold_method='otsu')`
Detect sunspots in an image.

**Parameters:**
- `image` (np.ndarray): Input image
- `min_area` (float): Minimum area threshold
- `max_area` (float): Maximum area threshold
- `threshold_method` (str): 'otsu' or 'binary'

**Returns:** List of Sunspot objects

#### `analyze_contours(image, min_area=50, max_area=None)`
Analyze contours and return statistics.

**Returns:** Tuple of (sunspots_list, statistics_dict)

### Sunspot Data Class

Each detected sunspot is a `Sunspot` object with:
- `area`: Area in pixels
- `perimeter`: Perimeter length
- `centroid`: (x, y) center coordinates
- `bounding_box`: (x, y, width, height)
- `contour`: OpenCV contour
- `circularity`: Shape measure (4π * area / perimeter²)
- `aspect_ratio`: Width/height ratio

### Utility Functions

- `load_image(path, as_grayscale=False)`: Load image from file
- `save_image(path, image)`: Save image to file
- `normalize_image(image, method='minmax')`: Normalize intensity values
- `resize_image(image, width=None, height=None, scale=None)`: Resize image
- `apply_clahe(image, clip_limit=2.0, tile_size=8)`: Contrast enhancement
- `gaussian_blur(image, kernel_size=5, sigma=1.0)`: Noise reduction

## Dependencies

- numpy >= 1.19.0
- opencv-python >= 4.5.0
- matplotlib >= 3.3.0
- scipy >= 1.5.0
- scikit-image >= 0.18.0
- Pillow >= 8.0.0

## Requirements

- Python >= 3.8
- For GPU acceleration: CUDA-compatible OpenCV build

## Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Citation

If you use this package in your research, please cite:

```bibtex
@software{sunspots2024,
  author = {Dey, Soumit},
  title = {Sunspots: Sunspot Detection and Analysis Package},
  year = {2024},
  url = {https://github.com/Soumit65/Sunspots}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- Bradley, D., & Roth, G. (2007). Adaptive Thresholding using the Integral Image. Journal of Graphics Tools, 12(2), 13-21.
- OpenCV Documentation: https://docs.opencv.org/

## Acknowledgments

- Developed as part of Summer 2024 Astronomy Internship
- Special thanks to the solar observation community
- OpenCV and NumPy communities for excellent tools

## Contact

- GitHub: [@Soumit65](https://github.com/Soumit65)
- Issues: [GitHub Issues](https://github.com/Soumit65/Sunspots/issues)

## Changelog

### Version 0.1.0 (2024)
- Initial release
- Bradley-Roth adaptive thresholding implementation
- Sunspot detection and area calculation
- Image processing utilities
- Documentation and examples
