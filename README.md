# Sunspots

> A Python toolkit for solar image analysis, sunspot detection, and feature characterization using modern image-processing techniques.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Astronomy](https://img.shields.io/badge/domain-solar%20physics-orange.svg)
[![GitHub](https://img.shields.io/badge/GitHub-Soumit65%2FSunspots-blue?logo=github)](https://github.com/Soumit65/Sunspots)

---

# About The Project

**Sunspots** is an open-source Python package developed during the **Astro Lab Summer Internship 2024** for analyzing solar imagery and detecting sunspots using modern image-processing techniques.

The project was originally created to explore how computational methods can be applied to real astronomical imaging data. Over time, it evolved into a reusable scientific toolkit for:

- solar image preprocessing
- adaptive thresholding
- feature extraction
- contour analysis
- quantitative sunspot measurements

The package combines astronomy and computer vision concepts into a beginner-friendly yet research-oriented framework.

---

# What Are Sunspots?

Sunspots are darker, cooler regions on the Sun’s surface caused by intense magnetic activity.

They are scientifically important because they help researchers study:

- solar magnetic fields
- solar cycles
- stellar activity
- space weather
- plasma dynamics

Analyzing sunspots helps scientists better understand solar behavior and its effects on Earth.

---

# How This Package Works

The workflow used in this package follows a standard astronomical image-analysis pipeline.

---

## Step 1 — Load Solar Images

The package first loads solar images from disk using OpenCV and NumPy.

```python
image = load_image("solar_image.jpg")
```

This converts the image into an array that can be processed mathematically.

---

## Step 2 — Image Preprocessing

Real astronomical images often contain:

- noise
- uneven brightness
- low contrast
- detector artifacts

To improve feature detection, preprocessing techniques are applied.

### CLAHE Contrast Enhancement

CLAHE (Contrast Limited Adaptive Histogram Equalization) improves local contrast while preventing over-amplification of noise.

```python
enhanced = apply_clahe(image)
```

Useful for making faint sunspots more visible.

---

### Gaussian Smoothing

Gaussian blur reduces high-frequency noise and smooths the image.

```python
smoothed = gaussian_blur(enhanced)
```

This helps prevent false detections.

---

### Image Normalization

Normalization rescales image intensities into a standard range.

```python
normalized = normalize_image(smoothed)
```

This improves thresholding consistency.

---

# Step 3 — Adaptive Thresholding

The core of the package is the **Bradley–Roth Adaptive Thresholding Algorithm**.

Traditional thresholding uses a single brightness cutoff across the entire image. This often fails for solar imagery because brightness varies across the solar disk.

Adaptive thresholding instead computes local intensity statistics around each pixel.

---

## Bradley–Roth Thresholding

The Bradley–Roth algorithm uses an **integral image** to efficiently compute local mean brightness values.

Pixels darker than their local neighborhood are classified as sunspots.

```python
binary = bradley_roth_threshold(
    image,
    block_size=51,
    constant=10
)
```

### Parameters

| Parameter | Meaning |
|---|---|
| `block_size` | Size of local neighborhood |
| `constant` | Sensitivity adjustment |
| `image` | Input solar image |

### Why It Matters

Solar images often have:

- radial brightness gradients
- atmospheric distortion
- non-uniform illumination

Adaptive thresholding handles these much better than global thresholding.

---

# 🧩 Step 4 — Contour Detection

Once thresholding produces a binary image, contours are extracted.

Contours represent connected regions of pixels identified as sunspots.

```python
spots = detect_sunspots(image)
```

Each contour is analyzed geometrically.

---

# 📊 Step 5 — Scientific Measurements

For every detected sunspot, the package calculates physical and geometric properties.

---

## Area

Measures the number of pixels occupied by the feature.

```python
spot.area
```

Useful for studying solar activity intensity.

---

## Perimeter

Measures boundary length.

```python
spot.perimeter
```

---

## Circularity

Quantifies how circular the feature is.

```python
spot.circularity
```

Computed using:

```math
4\pi A / P^2
```

where:

- \(A\) = area
- \(P\) = perimeter

Values close to 1 indicate nearly circular features.

---

## Centroid

Computes the center position of the sunspot.

```python
spot.centroid
```

Useful for tracking motion across solar observations.

---

## Bounding Box

Determines the smallest rectangle surrounding the feature.

```python
spot.bounding_box
```

Useful for cropping and visualization.

---

# Features

## Sunspot Detection

Automatically identify solar features using:

- Bradley–Roth adaptive thresholding
- Otsu thresholding
- Contour segmentation
- Morphological filtering

---

## Scientific Measurements

Compute quantitative properties including:

- area
- perimeter
- circularity
- aspect ratio
- centroids
- bounding boxes

---

## Image Processing Utilities

Built-in preprocessing tools include:

- CLAHE enhancement
- Gaussian smoothing
- normalization
- resizing
- grayscale conversion

---

## Simple API

Designed for both beginners and researchers.

```python
import sunspots

image = sunspots.load_image("solar_image.jpg")
spots = sunspots.detect_sunspots(image)

print(f"Detected {len(spots)} sunspots")
```

---

# Installation

## Install From Source

```bash
git clone https://github.com/Soumit65/Sunspots.git
cd Sunspots
pip install -e .
```

---

## Development Installation

```bash
pip install -e ".[dev,docs]"
```

---

## Planned PyPI Release

```bash
pip install sunspots
```

---

# Quick Start Example

```python
import sunspots
from sunspots import detect_sunspots, draw_sunspots

# Load image
image = sunspots.load_image("solar_image.jpg")

# Detect sunspots
spots = detect_sunspots(
    image,
    min_area=50,
    threshold_method="otsu"
)

# Draw detections
result = draw_sunspots(image, spots)

# Print statistics
for i, spot in enumerate(spots):
    print(f"Sunspot {i+1}")
    print(f"Area        : {spot.area:.2f}")
    print(f"Circularity : {spot.circularity:.3f}")
    print(f"Centroid    : {spot.centroid}")
```

---

# Example Analysis Pipeline

```python
from sunspots import (
    load_image,
    apply_clahe,
    gaussian_blur,
    detect_sunspots
)

# Load solar image
image = load_image("solar_image.jpg")

# Enhance image contrast
enhanced = apply_clahe(image)

# Remove noise
smoothed = gaussian_blur(enhanced)

# Detect features
spots = detect_sunspots(smoothed)

print(f"Detected {len(spots)} sunspots")
```

---

# Project Structure

```text
Sunspots/
│
├── sunspots/
│   ├── thresholding.py
│   ├── area_calculator.py
│   ├── utils.py
│   └── __init__.py
│
├── docs/
│   ├── installation.rst
│   ├── tutorials.rst
│   ├── examples.rst
│   └── api_reference.rst
│
├── notebooks/
├── README.md
├── pyproject.toml
└── LICENSE
```

---

# Documentation

The full documentation includes:

- installation guides
- tutorials
- worked examples
- API references
- preprocessing workflows
- thresholding explanations

Documentation website:

https://soumit65.github.io/Sunspots/

---

# Future Roadmap

Planned future features include:

- FITS file support
- solar limb-darkening correction
- active region tracking
- flare detection
- machine-learning segmentation
- time-series solar analysis
- interactive dashboards

---

# Contributing

Contributions are welcome.

```bash
git checkout -b feature/my-feature
git commit -m "Add new feature"
git push origin feature/my-feature
```

Then open a Pull Request.

---

# Citation

If you use this package in academic or research work, please cite:

```bibtex
@software{sunspots2024,
  author = {Dey, Soumit},
  title = {Sunspots: Solar Image Analysis Toolkit},
  year = {2024},
  url = {https://github.com/Soumit65/Sunspots}
}
```

---

# References

- Bradley, D., & Roth, G. (2007). *Adaptive Thresholding Using the Integral Image*. Journal of Graphics Tools, 12(2), 13–21.
- OpenCV Documentation: https://docs.opencv.org/

---

# Acknowledgments

- Developed during Astro Lab Summer Internship 2024
- Inspired by modern solar image-analysis workflows
- Built using the scientific Python ecosystem

---

# Contact

- GitHub: https://github.com/Soumit65
- Issues: https://github.com/Soumit65/Sunspots/issues

---

# License

Distributed under the MIT License. See `LICENSE` for details.
