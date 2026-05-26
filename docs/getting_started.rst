Getting Started
===============

Welcome to SuryaPy! This guide walks through the core workflow and concepts.

What is SuryaPy?
----------------

SuryaPy is a Python package for analyzing solar images to detect and measure sunspots.

Built on your internship research, it combines:

- **Bradley-Roth algorithm** — Fast adaptive thresholding using integral images
- **Morphological analysis** — Cleaning up noise via opening/closing
- **Connected components** — Finding individual sunspots via scipy.ndimage.label
- **Physical corrections** — Accounting for foreshortening and limb darkening
- **Unit conversions** — From pixels to standard solar physics measurements

No OpenCV — pure numpy, scipy, and astrolab.

Core Concepts
-------------

**Solar Disk Masking**
   Extract just the sun from the image. SuryaPy uses a simple threshold to find the bright solar disk, then crops to it.

**Bradley-Roth Thresholding**
   For each pixel, compute the mean intensity in a local window (size = image_width / Nx). Mark the pixel as foreground if it's darker than (local_mean × (100 - threshold) / 100). Uses an integral image (2D cumulative sum) for O(1) window queries.

**Morphological Cleanup**
   Remove noise and fill gaps:
   - **Binary opening**: Remove small bright regions
   - **Binary closing**: Fill holes in dark regions (sunspots)

**Connected Components**
   Find groups of connected dark pixels — each group is a potential sunspot. Label them and filter by size.

**Foreshortening Correction**
   Sunspots near the solar limb (edge) appear smaller due to projection angle. Correct with:

   .. math::
      A_{\text{corrected}} = \frac{A_{\text{observed}}}{\sqrt{1 - (y/R)^2 - (z/R)^2}}

   where y, z are the sunspot coordinates and R is the solar radius.

**Limb Darkening Correction**
   The sun's brightness decreases toward the edges (limb). SuryaPy corrects this by:
   1. Computing the median intensity at each distance from center
   2. Fitting a 3rd-degree polynomial to this radial profile
   3. Dividing each pixel by its fitted radial value

Standard Workflow
-----------------

The typical pipeline:

.. code-block:: python

   from astrolab import imaging as im
   from scipy import ndimage as scp
   import suryapy

   # 1. Load and preprocess
   image = im.load_image("DSC_1036.JPG")
   filtered = scp.gaussian_filter(image, sigma=0.5, radius=2)

   # 2. Mask and crop the solar disk
   cropped = suryapy.mask_sun(filtered, sun_threshold=50)

   # 3. Optional: correct limb darkening
   corrected = suryapy.limb_darkening_correction(cropped)

   # 4. Apply Bradley-Roth thresholding
   br_mask = suryapy.b_roth(cropped, threshold=9, Nx=100)

   # 5. Find and filter sunspots by connected component analysis
   labeled, n_comp, large, sizes, bbox = suryapy.find_components(
       br_mask, cropped, min_size=1000
   )

   # 6. Inspect a single component
   info = suryapy.inspect_component(1, labeled, n_comp, bbox, br_mask, cropped)

   # 7. Correct for foreshortening and convert to physical units
   y, z = -700, -900  # heliocentric coordinates
   area_px = info['area_pixels']
   area_corr = suryapy.foreshortening_correction(area_px, y=y, z=z)
   area_km2 = suryapy.pixels_to_km2(area_corr, km_per_pixel=458.58)
   area_mh = suryapy.km2_to_millionths(area_km2)

   print(f"Sunspot area: {area_mh:.2f} millionths of hemisphere")

Key Parameters to Tune
----------------------

**Threshold (b_roth)**

   - Default: 9
   - Range: 5–20
   - **Higher** → detect more (more aggressive)
   - **Lower** → fewer, larger spots

   Try 8–12 for typical DSLR solar images.

**Nx (b_roth window size)**

   - Default: 100 (window = image_width / 100)
   - **Smaller Nx** → larger window → smoother, might miss detail
   - **Larger Nx** → smaller window → more detail, more noise
   - Try 50–150 depending on image resolution.

**min_size (component filtering)**

   - Default: 1000 pixels
   - Removes components smaller than this
   - For a 4000×6000 DSLR image, 1000 pixels ≈ 0.2 mm at Earth
   - Adjust based on your image resolution and noise level.

**sun_threshold (mask_sun)**

   - Default: 50 (pixel value below which is not the sun)
   - Rarely needs changing; the sun is bright relative to background

Typical Workflow on Your Data
------------------------------

From the internship notebooks:

.. code-block:: python

   # Setup (from notebook)
   from astrolab import imaging as im
   from scipy import ndimage as scp
   import numpy as np
   import suryapy
   import matplotlib.pyplot as plt

   # Load DSLR and SIDC images
   raw_27 = im.load_image("DSC_1036.JPG")
   sidc_27 = im.load_image("27.JPG")

   # Preprocess with Gaussian filter
   filter_raw = scp.gaussian_filter(raw_27, sigma=0.5, radius=2)
   filter_sidc = scp.gaussian_filter(sidc_27, sigma=0.3, radius=2)

   image_list = [filter_raw, filter_sidc]
   rough_spot = [[-900, -700], [-250, 500]]

   # Process each image
   crops, spots = suryapy.process_image_list(image_list, rough_spot, print_log=True)

   # Now analyze
   cropped = crops[0]  # DSLR image
   br = suryapy.b_roth(cropped, threshold=9, Nx=100)

   # Find components
   labeled, n, large, sizes, bbox = suryapy.find_components(
       br, cropped, min_size=1000, print_log=True
   )

   # Inspect the first sunspot
   info = suryapy.inspect_component(1, labeled, n, bbox, br, cropped)
   print(f"Component 1: {info['area_pixels']} pixels")

   # Measure in physical units (DSLR calibration: 458.58 km/pixel)
   corrected = suryapy.foreshortening_correction(
       info['area_pixels'], y=-700, z=-900
   )
   mh = suryapy.km2_to_millionths(
       suryapy.pixels_to_km2(corrected, km_per_pixel=458.58)
   )
   print(f"Area: {mh:.2f} MH")

Next Steps
----------

- Try the :doc:`quick_start` (5 min)
- Read :doc:`tutorials` for deep dives (Bradley-Roth, limb darkening, etc.)
- Explore :doc:`examples` (complete notebook workflows)
- Reference :doc:`api_reference` (all functions)
- See :doc:`faq` (troubleshooting)
