=======================
Sunspots Documentation
=======================

Welcome to the Sunspots documentation! This package provides tools for detecting, tracking, and analyzing sunspots from solar images using adaptive thresholding and contour analysis.

**Sunspots** is a Python package designed for solar observation research and education, featuring the Bradley-Roth adaptive thresholding algorithm optimized for sunspot detection.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   installation
   api_reference
   tutorials
   examples
   faq

.. toctree::
   :maxdepth: 1
   :caption: Additional Resources:

   GitHub Repository <https://github.com/Soumit65/Sunspots>
   Issue Tracker <https://github.com/Soumit65/Sunspots/issues>
   PyPI Package <https://pypi.org/project/sunspots>

Features
========

✨ **Key Features**

- **Bradley-Roth Adaptive Thresholding**: Efficient algorithm for sunspot detection
- **Automatic Detection**: Identify sunspots with contour analysis
- **Area Calculation**: Precise measurements of sunspot areas
- **Property Analysis**: Circularity, aspect ratio, centroid, and more
- **Multiple Methods**: Otsu, Gaussian, and Mean thresholding support
- **Image Utilities**: Loading, normalization, enhancement functions
- **Easy API**: Simple functions for quick analysis

Quick Start
===========

Installation is easy:

.. code-block:: bash

   pip install sunspots

Basic usage:

.. code-block:: python

   import sunspots

   # Load and detect sunspots
   image = sunspots.load_image("solar_image.jpg")
   spots = sunspots.detect_sunspots(image)

   # Analyze results
   for spot in spots:
       print(f"Area: {spot.area}, Circularity: {spot.circularity:.3f}")

About
=====

Sunspots was developed as part of a 2024 Summer Astronomy Internship project. It combines solar observation research with practical computer vision techniques.

**License**: MIT

**Author**: Soumit Dey

**Citation**:

.. code-block:: bibtex

   @software{sunspots2024,
     author = {Dey, Soumit},
     title = {Sunspots: Sunspot Detection and Analysis Package},
     year = {2024},
     url = {https://github.com/Soumit65/Sunspots}
   }

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
