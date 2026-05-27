Examples
=========

This page contains a few example workflows using SuryaPy.

Basic Sunspot Detection
-----------------------

.. code-block:: python

   import matplotlib.pyplot as plt

   from suryapy import (
       mask_sun,
       b_roth,
       find_components,
   )

   image = plt.imread("solar_image.jpg")

   if image.ndim == 3:
       image = image.mean(axis=2)

   cropped = mask_sun(image)

   br_mask = b_roth(
       cropped,
       threshold=10,
       Nx=100,
   )

   (
       labeled_image,
       num_components,
       large_components_mask,
       component_sizes,
       bound_box,
   ) = find_components(
       br_mask,
       cropped,
       min_size=100,
   )

Displaying Detected Sunspots
----------------------------

.. code-block:: python

   plt.figure(figsize=(8,8))

   plt.imshow(cropped, cmap="inferno")

   plt.contour(
       large_components_mask,
       colors='cyan',
       linewidths=1.2
   )

   plt.title("Detected Sunspots")

   plt.axis("off")

.. image:: images/detected_sunspots_overlay.png
   :width: 700px
   :align: center

Area Distribution
-----------------

.. code-block:: python

   valid_sizes = component_sizes[component_sizes > 100]

   plt.figure(figsize=(7,5))

   plt.hist(valid_sizes, bins=20)

   plt.xlabel("Sunspot Area (pixels)")
   plt.ylabel("Count")

   plt.title("Distribution of Sunspot Areas")

.. image:: images/area_distribution.png
   :width: 650px
   :align: center

Foreshortening Correction
-------------------------

.. code-block:: python

   from suryapy import foreshortening_correction

   corrected_area = foreshortening_correction(
       area_pixels=1276,
       y=-700,
       z=-900,
   )

   print(corrected_area)

Area Conversion
---------------

.. code-block:: python

   from suryapy import (
       pixels_to_km2,
       km2_to_millionths,
   )

   area_km2 = pixels_to_km2(
       area_pixels=5000,
       km_per_pixel=458.58,
   )

   area_mh = km2_to_millionths(area_km2)

   print(area_mh)

Batch Processing
----------------

SuryaPy can also process multiple solar images in sequence.

.. code-block:: python

   image_list = [
       "image_01.jpg",
       "image_02.jpg",
       "image_03.jpg",
   ]

   for filename in image_list:

       image = plt.imread(filename)

       cropped = mask_sun(image)

       br_mask = b_roth(cropped, threshold=10)

       print(f"Processed: {filename}")

Future Examples
---------------

Additional tutorials and examples may include:

- solar image time series
- automatic tracking
- FITS file workflows
- limb-darkening correction
- comparison with professional solar datasets
