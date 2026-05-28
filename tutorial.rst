Tutorials
=========

These tutorials explain the core image-processing and solar-physics techniques used inside SuryaPy.

The methods were developed during the Astro Lab Summer Internship 2024 at Ashoka University.

The workflow is divided into two major parts:

1. **Sunspot Tracking**
2. **Sunspot Area Measurement**

|

Part I — Sunspot Tracking
=========================

Tracking sunspots across multiple observations allows us to:

- estimate solar rotation
- monitor spot evolution
- align observations between frames
- compare DSLR observations against SIDC data

|

Tracking Workflow
-----------------

The tracking pipeline is:

1. Load solar image
2. Detect solar disk
3. Crop the solar disk
4. Find target sunspot centroid
5. Repeat for multiple images
6. Compare spot motion

|

Original Solar Observation
--------------------------

.. image:: images/original_solar_image.png
   :width: 700px
   :align: center

|

Solar Disk Detection
--------------------

The first step is identifying the solar disk boundary.

SuryaPy masks the background and isolates the Sun automatically.

.. image:: images/solar_disc_detection.png
   :width: 700px
   :align: center

|

Masking and Cropping
--------------------

The solar disk is cropped for easier processing.

.. image:: images/masked_solar_disc.png
   :width: 700px
   :align: center

|

Tracking a Sunspot
------------------

A target sunspot is identified using centroid-finding methods built on top of ``astrolab``.

.. code-block:: python

   import suryapy
   from astrolab import imaging as im

   image = im.load_image("DSC_1036.JPG")

   cropped = suryapy.mask_sun(
       image,
       sun_threshold=50
   )

   spot = suryapy.find_spot(
       cropped,
       spot_pos=[-900, -700],
       search=100
   )

   print(spot)

|

Processing a Single Image
-------------------------

The ``process`` function combines cropping and spot-finding.

.. code-block:: python

   cropped, spot_centroid = suryapy.process(
       image,
       spot_pos=[-900, -700],
       print_log=True
   )

|

Tracking Across Multiple Images
-------------------------------

Multiple observations can be processed automatically.

.. code-block:: python

   images = [image1, image2, image3]

   positions = [
       [-900, -700],
       [-850, -650],
       [-800, -620]
   ]

   crops, spots = suryapy.process_image_list(
       images,
       positions
   )

|

Tracking Visualization
----------------------

.. image:: images/detected_sunspots_overlay.png
   :width: 700px
   :align: center

|

Coordinate System
-----------------

SuryaPy uses solar-radius coordinates:

- origin at solar disk center
- x and y range approximately from ``-R`` to ``+R``

This is useful for physical calculations like:

- angular distance
- heliographic location
- foreshortening correction

|

Angular Distance
----------------

The angular distance of a spot from disk center can be computed as:

.. code-block:: python

   angular_deg = suryapy.angular_distance(
       x_spot=0,
       y_spot=1000,
       pixel_radius=1516
   )

|

Part II — Sunspot Area Measurement
==================================

After locating sunspots, the next step is measuring their physical area.

This requires:

1. Thresholding
2. Morphological cleanup
3. Connected-component analysis
4. Foreshortening correction
5. Physical unit conversion

|

Bradley-Roth Adaptive Thresholding
----------------------------------

Bradley-Roth converts a grayscale image into a binary mask using adaptive local thresholds.

This is particularly effective for solar images because illumination changes across the solar disk.

.. image:: images/bradley_roth_threshold.png
   :width: 700px
   :align: center

|

Using Bradley-Roth
------------------

.. code-block:: python

   br = suryapy.b_roth(
       cropped,
       threshold=9,
       Nx=100
   )

|

Parameter Tuning
----------------

+-------------+-------------------------------------------+---------------+
| Parameter   | Effect                                    | Typical Range |
+=============+===========================================+===============+
| threshold   | Detection sensitivity                     | 5–20          |
+-------------+-------------------------------------------+===============+
| Nx          | Window divisor                            | 50–150        |
+-------------+-------------------------------------------+---------------+

|

Thresholding Results
--------------------

.. image:: images/bradley_roth_clean.png
   :width: 700px
   :align: center

|

Limb Darkening Correction
-------------------------

The solar limb appears darker because observations probe cooler upper layers of the photosphere.

Without correction:

- spots near the limb become harder to detect
- thresholding becomes biased
- segmentation quality decreases

|

Intensity Profile
-----------------

.. image:: images/intensity_histogram.png
   :width: 700px
   :align: center

|

Correction Model
----------------

The radial brightness profile is approximated using a polynomial:

:contentReference[oaicite:0]{index=0}

|

Applying the Correction
-----------------------

.. code-block:: python

   corrected = suryapy.limb_darkening_correction(
       cropped,
       show_plot=True
   )

|

Connected Component Analysis
----------------------------

Once thresholded, individual sunspots are identified using connected-component labeling.

.. image:: images/connected_components.png
   :width: 700px
   :align: center

|

Morphological Cleanup
---------------------

Small noisy structures are removed using binary morphology.

.. code-block:: python

   from scipy import ndimage as scp
   import numpy as np

   struct = np.ones((3, 3))

   opened = scp.binary_opening(
       br_mask,
       structure=struct
   )

   closed = scp.binary_closing(
       br_mask,
       structure=struct
   )

|

Labeling Components
-------------------

.. code-block:: python

   labeled, n = scp.label(
       closed == 0
   )

|

Using SuryaPy
-------------

.. code-block:: python

   labeled, n, large_mask, sizes, bbox = suryapy.find_components(
       br_mask,
       cropped,
       min_size=1000,
       print_log=True
   )

|

Labelled Components
-------------------

.. image:: images/labelled_components.png
   :width: 700px
   :align: center

|

Inspecting Individual Components
--------------------------------

Each detected sunspot can be inspected individually.

.. code-block:: python

   info = suryapy.inspect_component(
       target_label=77,
       labeled_image=labeled,
       num_components=n,
       bound_box=bbox,
       br_mask=br_mask,
       image=cropped
   )

|

Component Inspection
--------------------

.. image:: images/component_inspection.png
   :width: 700px
   :align: center

|

Foreshortening Correction
-------------------------

Sunspots near the solar limb appear geometrically compressed.

Their observed area must be corrected.

|

Correction Formula
------------------

:contentReference[oaicite:1]{index=1}

|

Applying the Correction
-----------------------

.. code-block:: python

   corrected_area = suryapy.foreshortening_correction(
       area_pixels=1276,
       y=-700,
       z=-900,
       R_sun=1511
   )

|

Pixel Area to km²
-----------------

Observed areas depend on instrument calibration.

From the internship calibration:

+-------------------+------------------+
| Instrument        | km / pixel       |
+===================+==================+
| DSLR              | 458.58           |
+-------------------+------------------+
| SIDC              | 738.44           |
+-------------------+------------------+

|

Conversion Example
------------------

.. code-block:: python

   area_km2 = suryapy.pixels_to_km2(
       corrected_area,
       km_per_pixel=458.58
   )

|

Millionths of Hemisphere (MH)
-----------------------------

Solar physicists commonly use millionths of solar hemisphere (MH).

.. code-block:: python

   area_mh = suryapy.km2_to_millionths(
       area_km2
   )

   print(area_mh)

|

Area Distribution
-----------------

.. image:: images/area_distribution.png
   :width: 700px
   :align: center

|

Complete Pipeline
-----------------

The full SuryaPy workflow combines:

- solar disk detection
- preprocessing
- tracking
- thresholding
- component analysis
- physical corrections
- unit conversion

.. image:: images/suryapy_pipeline.png
   :width: 900px
   :align: center

|

Complete Example
----------------

.. code-block:: python

   import suryapy as sio
   from astrolab import imaging as im
   from scipy import ndimage as scp

   # Load image
   raw = im.load_image("DSC_1036.JPG")

   # Smooth image
   filtered = scp.gaussian_filter(
       raw,
       sigma=0.5
   )

   # Crop solar disk
   cropped = sio.mask_sun(filtered)

   # Limb darkening correction
   corrected = sio.limb_darkening_correction(
       cropped
   )

   # Bradley-Roth thresholding
   br = sio.b_roth(
       corrected,
       threshold=9
   )

   # Connected components
   labeled, n, large, sizes, bbox = sio.find_components(
       br,
       corrected,
       min_size=1000
   )

   # Inspect first component
   info = sio.inspect_component(
       1,
       labeled,
       n,
       bbox,
       br,
       corrected
   )

   # Area correction
   area_px = info['area_pixels']

   area_corr = sio.foreshortening_correction(
       area_px,
       y=-700,
       z=-900
   )

   # Convert to physical units
   area_km2 = sio.pixels_to_km2(
       area_corr,
       km_per_pixel=458.58
   )

   area_mh = sio.km2_to_millionths(
       area_km2
   )

   print(f"Sunspot area: {area_mh:.2f} MH")
