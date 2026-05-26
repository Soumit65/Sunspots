Quick Start (5 Minutes)
======================

Install
-------

.. code-block:: bash

   pip install -e "path/to/SuryaPy"

Or from source:

.. code-block:: bash

   git clone https://github.com/Soumit65/SuryaPy.git
   cd SuryaPy
   pip install -e .

Basic Sunspot Detection
-----------------------

.. code-block:: python

   from astrolab import imaging as im
   from scipy import ndimage as scp
   import suryapy

   # Load a solar image
   image = im.load_image("solar_image.jpg")

   # Smooth it
   smooth = scp.gaussian_filter(image, sigma=0.5, radius=2)

   # Isolate the sun and crop
   cropped = suryapy.mask_sun(smooth)

   # Apply Bradley-Roth thresholding
   br_mask = suryapy.b_roth(cropped, threshold=9, Nx=100, print_log=False)

   # Find sunspots (connected components)
   labeled, n_components, large_mask, sizes, bbox = suryapy.find_components(
       br_mask, cropped, min_size=1000, print_log=False
   )

   # Count spots
   print(f"Found {n_components} components, {len([s for s in sizes if s >= 1000])} are large")

   # Measure the first one
   info = suryapy.inspect_component(1, labeled, n_components, bbox, br_mask, cropped, print_log=False)
   print(f"Spot 1: {info['area_pixels']} pixels")

Get Area in Standard Units
---------------------------

.. code-block:: python

   # Correct for where the sunspot is on the disk
   y, z = -700, -900  # heliocentric coordinates (pixels)

   corrected_area = suryapy.foreshortening_correction(
       info['area_pixels'],
       y=y, z=z,
       R_sun=1511
   )

   # Convert to km²
   area_km2 = suryapy.pixels_to_km2(
       corrected_area,
       km_per_pixel=458.58  # DSLR calibration from your data
   )

   # Convert to millionths of solar hemisphere (MH)
   area_mh = suryapy.km2_to_millionths(area_km2)

   print(f"Sunspot area: {area_mh:.2f} millionths of hemisphere")

Track a Spot Across Multiple Images
------------------------------------

.. code-block:: python

   # Load several images
   images = [
       im.load_image("image1.jpg"),
       im.load_image("image2.jpg"),
       im.load_image("image3.jpg"),
   ]

   # Rough positions (you provide these)
   rough_positions = [
       [-900, -700],
       [-850, -700],
       [-800, -700],
   ]

   # Preprocess all
   filtered = [scp.gaussian_filter(img, sigma=0.5, radius=2) for img in images]

   # Process (crop + find centroid)
   crops, centroids = suryapy.process_image_list(
       filtered, rough_positions, print_log=True
   )

   print(f"Centroids across images:\n{centroids}")

Remove Limb Darkening
---------------------

.. code-block:: python

   # Correct for the sun's brightness falloff toward the edges
   corrected = suryapy.limb_darkening_correction(cropped, show_plot=True)

   # Now threshold the corrected image
   br_mask = suryapy.b_roth(corrected, threshold=9, Nx=100)

Common Mistakes
---------------

❌ **Forgetting to preprocess**

   Raw DSLR images are noisy. Always filter first:

   .. code-block:: python

      filtered = scp.gaussian_filter(image, sigma=0.5, radius=2)  # Good!

❌ **Using wrong coordinates for foreshortening**

   y and z must be in **pixels from the disc center**, not image coordinates:

   .. code-block:: python

      # WRONG (these are image pixel coords)
      suryapy.foreshortening_correction(area, y=1500, z=2000)

      # RIGHT (these are solar-radius pixel coords, range ±1511)
      suryapy.foreshortening_correction(area, y=-700, z=-900)

❌ **Threshold too aggressive**

   If you're getting weird detection results, try lowering threshold (5–8) instead of raising it.

   .. code-block:: python

      br = suryapy.b_roth(cropped, threshold=5)  # Less aggressive

💡 Tips
------

- **Preprocess always**: Gaussian filter + optional limb darkening correction
- **Start with threshold=9**: Adjust up/down by 1–2 if needed
- **Check min_size**: Raise it if you're getting noise; lower if missing small spots
- **Visualize intermediates**: Use ``print_log=True`` to see what's happening
- **Calibrate once**: Measure your instrument's km/pixel once, reuse it

Next: Explore :doc:`tutorials` for detailed algorithm explanations.
