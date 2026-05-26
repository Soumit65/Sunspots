FAQ
===

General Questions
-----------------

**Q: What is SuryaPy?**

A: SuryaPy is a Python package for detecting and measuring sunspots from solar images. It combines the Bradley-Roth adaptive thresholding algorithm (from your internship) with connected component analysis, physical corrections, and unit conversions. Built on astrolab, numpy, and scipy — no OpenCV.

**Q: Who should use SuryaPy?**

A: Astronomy researchers, students, solar observation hobbyists, and anyone analyzing solar images.

**Q: Is SuryaPy free?**

A: Yes! MIT licensed, open source.

**Q: Why "SuryaPy"?**

A: *Surya* is the Sun in Sanskrit. Python package. 🌞

Installation & Setup
--------------------

**Q: How do I install SuryaPy?**

A: Clone and install in editable mode:

.. code-block:: bash

   git clone https://github.com/Soumit65/SuryaPy.git
   cd SuryaPy
   pip install -e .

**Q: I get "ModuleNotFoundError: astrolab"**

A: Install astrolab (your college's solar imaging library):

.. code-block:: bash

   # From your college's repo
   git clone https://github.com/your-college/astrolab.git
   cd astrolab
   pip install -e .

Check astrolab docs for details.

**Q: What's the difference between "pip install -e ." and "pip install ."?**

A: 
- ``pip install -e .`` (editable): Changes to code take effect immediately. Good for development.
- ``pip install .`` (normal): Copies the package. Good for release versions.

**Q: Can I use SuryaPy in a virtual environment?**

A: Recommended:

.. code-block:: bash

   python -m venv suryapy_env
   source suryapy_env/bin/activate
   pip install -e "path/to/SuryaPy"

Usage Questions
---------------

**Q: What threshold value should I use?**

A: Start with 9. Adjust based on results:
   - 5–8: Conservative (fewer detections, larger spots)
   - 9–12: Balanced (typical)
   - 13–20: Aggressive (more detections, including noise)

Try 8–9 first, then tune up/down by 1.

**Q: What does min_size do?**

A: Filters out components smaller than ``min_size`` pixels. Removes noise and very small features. Typical: 500–2000 pixels depending on image resolution.

**Q: My spots aren't being detected. What do I do?**

A: Try, in order:

1. Lower threshold (8 → 5)
2. Increase Nx (100 → 50, larger window)
3. Decrease min_size (1000 → 500)
4. Add preprocessing: ``limb_darkening_correction()`` before ``b_roth()``
5. Apply Gaussian filter: ``scp.gaussian_filter(image, sigma=0.5, radius=2)``

**Q: I'm getting too many false positives (noise)**

A: Try:

1. Raise min_size (1000 → 2000)
2. Increase threshold (9 → 12)
3. Lower Nx (100 → 150, smaller window)
4. Add stronger Gaussian blur: ``scp.gaussian_filter(image, sigma=1.0, radius=4)``

**Q: What are "solar-radius pixel coordinates"?**

A: Pixels measured from the disc center, ranging from -R to +R (e.g., -1511 to +1511). Not image pixel coordinates (which start at 0). The ``process()`` and ``find_spot()`` functions return solar-radius coords automatically.

**Q: How do I find the heliocentric coordinates of a spot?**

A: Either:

1. Use ``find_spot()`` (returns centroid in solar-radius coords)
2. Estimate from component bounding box: midpoint of y/x coordinates

.. code-block:: python

   info = suryapy.inspect_component(...)
   y_center = (info['y_start'] + info['y_end']) / 2
   z_center = (info['x_start'] + info['x_end']) / 2

**Q: What's the difference between "foreshortening" and "limb darkening"?**

A: 
- **Foreshortening**: Spots near the solar edge appear *smaller* due to projection angle. Correction multiplies by ~1.01–1.5.
- **Limb darkening**: The sun's brightness *decreases* toward the edge (cooler upper layers). Correction divides pixel values by a radial profile.

Use both for best results.

**Q: How do I convert pixels to standard units?**

A: Three-step process:

1. Correct for foreshortening: ``foreshortening_correction(area, y, z)``
2. Convert pixels → km²: ``pixels_to_km2(area, km_per_pixel=458.58)``
3. Convert km² → millionths of hemisphere: ``km2_to_millionths(area)``

.. code-block:: python

   corrected = suryapy.foreshortening_correction(1276, y=-700, z=-900)
   km2 = suryapy.pixels_to_km2(corrected, km_per_pixel=458.58)
   mh = suryapy.km2_to_millionths(km2)
   print(f"{mh:.2f} MH")

**Q: What's my instrument's km/pixel value?**

A: From your internship:
- DSLR: 458.58 km/pixel
- SIDC: 738.44 km/pixel

For other instruments, calibrate once using a reference (e.g., known sunspot size, sun angular radius).

Technical Questions
-------------------

**Q: Does SuryaPy use OpenCV?**

A: No. Pure numpy, scipy, matplotlib, and astrolab. This avoids OpenCV dependency and complexity.

**Q: What's the Bradley-Roth algorithm?**

A: An adaptive thresholding algorithm that compares each pixel to the *local* mean (not global). Uses an integral image for O(1) window queries. See :doc:`tutorials` for details.

**Q: How does connected component analysis work?**

A: After thresholding, we get a binary image (0/1). Scipy's ``ndimage.label()`` assigns each connected region of pixels a unique label. We then filter by size. See :doc:`tutorials` for details.

**Q: Why is my thresholded image inverted?**

A: Sunspots are dark (low pixel values), so the Bradley-Roth algorithm marks them as 0 (background). Bright regions are 1 (foreground). When you display with cmap='gray', 0 = black, 1 = white. This is correct — sunspots appear black.

**Q: Can I use SuryaPy with other astrolab functions?**

A: Absolutely. SuryaPy functions accept numpy arrays. You can mix:

.. code-block:: python

   img = im.load_image("file.jpg")  # astrolab
   cropped = suryapy.mask_sun(img)  # suryapy
   filtered = scp.gaussian_filter(cropped, sigma=0.5)  # scipy
   result = suryapy.b_roth(filtered)  # suryapy

Performance & Troubleshooting
-----------------------------

**Q: Processing is slow. How do I speed it up?**

A: Try:

1. Resize images: ``im.crop(image, scale=0.5)`` (4× faster)
2. Increase Nx (larger windows, faster): 100 → 50
3. Decrease image resolution
4. Use GPU (if your OpenCV is built with CUDA) — though SuryaPy doesn't use CUDA yet

**Q: Why is my corrected area almost the same as the observed area?**

A: The foreshortening correction only matters far from disc center. For a spot near center (y ≈ 0, z ≈ 0), the correction is ~1.0 (no change). For a spot near the limb (y²+z² → R²), correction is large.

**Q: I'm getting NaN or infinite values. Why?**

A: Check:

1. Division by zero: ``foreshortening_correction`` will give NaN if y²+z² ≥ R²(spot beyond limb, shouldn't happen).
2. Empty components: Make sure ``labeled_image`` has components before calling ``inspect_component``.
3. Bad calibration: km_per_pixel = 0 will cause NaN in ``pixels_to_km2``.

Contributing & Citation
-----------------------

**Q: Can I contribute to SuryaPy?**

A: Yes! Fork the repo, create a branch, commit, and open a PR. See README for guidelines.

**Q: How do I cite SuryaPy in my paper?**

A:

.. code-block:: bibtex

   @software{suryapy2024,
     author = {Dey, Soumit},
     title = {SuryaPy: Solar Sunspot Detection and Analysis},
     year = {2024},
     url = {https://github.com/Soumit65/SuryaPy}
   }

**Q: Can I use SuryaPy commercially?**

A: Yes. MIT license allows it. Just include the license text in your distribution.

**Q: Where do I report bugs?**

A: GitHub Issues: https://github.com/Soumit65/SuryaPy/issues

Include:
- Code snippet to reproduce
- Error message
- Your Python/astrolab versions
- What you expected vs. what happened

Example Problems
----------------

**Problem: "AttributeError: module 'astrolab.imaging' has no attribute 'find_star'"**

- Your astrolab version is missing ``find_star``. Check astrolab docs and update.

**Problem: "ValueError: x and y arrays don't match in size" (in limb darkening)**

- The image might be non-square. limb_darkening_correction assumes a square (or nearly square) image centered on the sun.

**Problem: Results differ between runs**

- Unlikely unless you're using randomness (you're not in SuryaPy). Check if threshold/Nx/min_size changed.

Still Stuck?
------------

1. Check :doc:`getting_started` and :doc:`quick_start`
2. Search :doc:`tutorials` for your topic
3. Browse :doc:`examples` for similar workflows
4. Check :doc:`api_reference` for function details
5. Open a GitHub Issue with details
6. Ask on your college's astronomy forum

Let's observe the sun. ☀️
