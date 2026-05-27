API Reference
==============

Thresholding Functions
----------------------

mask_sun
^^^^^^^^

.. code-block:: python

   mask_sun(
       image_array,
       sun_threshold=50,
       print_log=False,
       crop=True,
   )

Detects and crops the solar disc from an image.

Parameters
"""""""""""

- ``image_array`` : 2D image array
- ``sun_threshold`` : threshold separating Sun from background
- ``print_log`` : display diagnostic plots
- ``crop`` : return cropped image

Returns
"""""""

Cropped solar image or mask information.

b_roth
^^^^^^

.. code-block:: python

   b_roth(
       image_main,
       threshold,
       Nx=100,
       print_log=True,
   )

Bradley–Roth adaptive thresholding using integral images.

Parameters
"""""""""""

- ``image_main`` : grayscale solar image
- ``threshold`` : sensitivity parameter
- ``Nx`` : sliding window divisor
- ``print_log`` : display thresholded result

Returns
"""""""

Binary threshold mask.

Connected Component Functions
-----------------------------

find_components
^^^^^^^^^^^^^^^

.. code-block:: python

   find_components(
       br_mask,
       image,
       min_size=1000,
       print_log=True,
   )

Find connected sunspot regions using ``scipy.ndimage.label``.

Returns:

- labelled image
- component count
- filtered mask
- component sizes
- bounding boxes

inspect_component
^^^^^^^^^^^^^^^^^

.. code-block:: python

   inspect_component(
       target_label,
       labeled_image,
       num_components,
       bound_box,
       br_mask,
       image,
   )

Display and inspect an individual detected sunspot region.

Correction Functions
--------------------

foreshortening_correction
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   foreshortening_correction(
       area_pixels,
       y,
       z,
       R_sun=1511,
   )

Corrects measured areas for projection effects near the solar limb.

pixels_to_km2
^^^^^^^^^^^^^

.. code-block:: python

   pixels_to_km2(
       area_pixels,
       km_per_pixel,
   )

Convert pixel areas into physical km².

km2_to_millionths
^^^^^^^^^^^^^^^^^

.. code-block:: python

   km2_to_millionths(
       area_km2,
       R_sun_km=696000,
   )

Convert km² into millionths of the solar hemisphere.

angular_distance
^^^^^^^^^^^^^^^^

.. code-block:: python

   angular_distance(
       x_spot,
       y_spot,
       pixel_radius=1516,
       angular_radius_deg=0.27,
   )

Estimate angular distance from the solar disc centre.

Tracking Utilities
------------------

tracking.py contains experimental tools for:

- tracking sunspots between frames
- processing image sequences
- solar evolution studies

These APIs may change in future releases.

Package Information
-------------------

Current version:

.. code-block:: python

   import suryapy

   print(suryapy.__version__)
