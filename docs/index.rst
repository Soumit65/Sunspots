=======================
SuryaPy Documentation
=======================

**SuryaPy** — Solar sunspot detection and analysis, from *Surya* (the Sun).

A Python package for detecting, analyzing, and measuring sunspots from solar observations using adaptive thresholding, connected component analysis, and physical corrections.

Built from your 2024 summer astronomy internship work. Uses the Bradley-Roth integral-image algorithm, astrolab for I/O, and scipy.ndimage for morphology.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   getting_started
   installation
   quick_start

.. toctree::
   :maxdepth: 2
   :caption: Learn:

   tutorials
   examples
   api_reference
   faq

.. toctree::
   :maxdepth: 1
   :caption: Resources:

   GitHub Repository <https://github.com/Soumit65/SuryaPy>
   Issue Tracker <https://github.com/Soumit65/SuryaPy/issues>

Key Features
============

✨ **Bradley-Roth Adaptive Thresholding**
   Integral-image based algorithm for detecting dark regions (sunspots) on bright background

🎯 **Connected Component Analysis**
   Automatic sunspot identification via morphological cleanup + scipy.ndimage.label

🔬 **Physical Corrections**
   - Foreshortening correction (projection angle)
   - Limb darkening removal (radial intensity profile)
   - Pixel-to-km² and km² to millionths of hemisphere (MH)

📍 **Spot Tracking**
   Integration with astrolab for multi-image centroid finding and registration

📊 **Standard Solar Physics Units**
   Automatic conversion to millionths of solar hemisphere (MH), angular distances

Quick Example
=============

Detect sunspots in 10 lines:

.. code-block:: python

   from astrolab import imaging as im
   from scipy import ndimage as scp
   import suryapy

   # Load and filter
   raw = im.load_image("solar.jpg")
   filtered = scp.gaussian_filter(raw, sigma=0.5, radius=2)

   # Detect
   cropped = suryapy.mask_sun(filtered)
   br_mask = suryapy.b_roth(cropped, threshold=9)
   labeled, n, large, sizes, bbox = suryapy.find_components(br_mask, cropped)

   # Measure
   for i, size in enumerate(sizes):
       print(f"Sunspot {i+1}: {size} pixels")

What's Inside
=============

.. code-block:: text

   sunspots/
   ├── thresholding.py  — b_roth, mask_sun
   ├── tracking.py      — find_spot, process, display_spot
   ├── correction.py    — limb_darkening_correction
   └── area.py         — find_components, foreshortening, unit conversion

Installation
============

From source (recommended):

.. code-block:: bash

   git clone https://github.com/Soumit65/SuryaPy.git
   cd SuryaPy
   pip install -e .

With docs and dev tools:

.. code-block:: bash

   pip install -e ".[dev,docs,jupyter]"

Dependencies
============

- **astrolab** — Your college's solar imaging library (required!)
- **numpy**, **scipy**, **matplotlib** — Scientific Python stack
- **Python 3.8+** — Modern Python

No OpenCV. Pure astrolab + numpy/scipy.

Next Steps
==========

- Read :doc:`getting_started` to understand the workflow
- Try :doc:`quick_start` for a runnable 5-minute intro
- Explore :doc:`tutorials` for deep dives into algorithms
- Check :doc:`examples` for real notebook workflows
- See :doc:`api_reference` for complete function docs

About
=====

Developed during the **2024 Summer Astronomy Internship** as part of your research on sunspot detection and solar observation.

**License**: MIT (open source, free to use and modify)

**Author**: Soumit Dey

**Citation**:

.. code-block:: bibtex

   @software{suryapy2024,
     author = {Dey, Soumit},
     title = {SuryaPy: Solar Sunspot Detection and Analysis},
     year = {2024},
     url = {https://github.com/Soumit65/SuryaPy}
   }

Let's observe the sun. ☀️
