API Reference
=============

Thresholding Module
-------------------

.. py:module:: sunspots.thresholding

.. py:function:: b_roth(image_main, threshold, Nx=100, print_log=True)

   Bradley-Roth adaptive thresholding using integral images.

   For each pixel, computes the local mean over a window using 2D cumulative sum, then marks
   the pixel as foreground if it exceeds ``local_mean × (100 - threshold) / 100``.

   **Parameters:**

   - ``image_main`` (np.ndarray): 2D grayscale image (e.g., from mask_sun or im.load_image)
   - ``threshold`` (float): Sensitivity (5–20 typical). Higher = detect more.
   - ``Nx`` (int, optional): Window divisor. Window = image_width // Nx. Default 100.
   - ``print_log`` (bool, optional): Display result. Default True.

   **Returns:**

   - np.ndarray: Binary image (0/1), same shape as input

   **Example:**

   .. code-block:: python

      br_mask = suryapy.b_roth(cropped, threshold=9, Nx=100)

.. py:function:: mask_sun(image_array, sun_threshold=50, print_log=False, crop=True)

   Create a mask isolating the solar disk and optionally crop.

   Finds the sun's edges using row/column means of a threshold mask, then crops using astrolab's im.crop.

   **Parameters:**

   - ``image_array`` (np.ndarray): 2D image array
   - ``sun_threshold`` (float, optional): Pixel value below which is background. Default 50.
   - ``print_log`` (bool, optional): Display edges and histogram. Default False.
   - ``crop`` (bool, optional): Return cropped image (True) or coordinates (False). Default True.

   **Returns:**

   - np.ndarray: Cropped image (if crop=True), or tuple (left, right, top, bottom, mask)

   **Example:**

   .. code-block:: python

      cropped = suryapy.mask_sun(filtered_image, crop=True)
      left, right, top, bottom, mask = suryapy.mask_sun(image, crop=False)

Tracking Module
---------------

.. py:module:: sunspots.tracking

.. py:function:: find_spot(array, spot_pos, search=100, print_log=False, fig=None, ax=None)

   Locate a sunspot centroid using astrolab's im.find_star on the inverted image.

   Sunspots are dark, so the image is inverted before passing to find_star (which expects bright objects).

   **Parameters:**

   - ``array`` (np.ndarray): 2D cropped/masked image
   - ``spot_pos`` (tuple or list): Approximate [x, y] spot position in solar-radius coords
   - ``search`` (int, optional): Search box half-width in pixels. Default 100.
   - ``print_log`` (bool, optional): Display marked result. Default False.
   - ``fig``, ``ax`` (optional): Matplotlib figure/axes for display

   **Returns:**

   - tuple: (x, y) centroid position

   **Example:**

   .. code-block:: python

      centroid = suryapy.find_spot(cropped, spot_pos=[-900, -700])

.. py:function:: process(image, spot_pos, print_log=False, fig=None, ax=None)

   Full single-image pipeline: mask/crop the sun, then find a spot.

   **Parameters:**

   - ``image`` (np.ndarray): Raw solar image
   - ``spot_pos`` (tuple): Approximate [x, y] position
   - ``print_log`` (bool, optional): Display intermediates. Default False.

   **Returns:**

   - tuple: (cropped_image, spot_centroid)

   **Example:**

   .. code-block:: python

      cropped, centroid = suryapy.process(raw_image, spot_pos=[-900, -700], print_log=True)

.. py:function:: process_image_list(image_list, rough_spot_list, print_log=True)

   Process multiple images, returning crops and centroids for each.

   **Parameters:**

   - ``image_list`` (list of np.ndarray): Filtered images
   - ``rough_spot_list`` (list of tuple): Approximate positions, one per image
   - ``print_log`` (bool, optional): Display each. Default True.

   **Returns:**

   - tuple: (crop_list, spot_array) where spot_array is shape (N, 2)

   **Example:**

   .. code-block:: python

      crops, spots = suryapy.process_image_list(
          [img1, img2, img3],
          [[-900, -700], [-250, 500], [220, 450]]
      )

Correction Module
-----------------

.. py:module:: sunspots.correction

.. py:function:: limb_darkening_correction(image, show_plot=False)

   Remove limb darkening via radial median intensity profile and 3rd-degree polynomial fit.

   **Parameters:**

   - ``image`` (np.ndarray): 2D image (float or int)
   - ``show_plot`` (bool, optional): Display corrected image. Default False.

   **Returns:**

   - np.ndarray: Corrected image (float), same shape

   **Example:**

   .. code-block:: python

      corrected = suryapy.limb_darkening_correction(cropped, show_plot=True)

Area Module
-----------

.. py:module:: sunspots.area

.. py:function:: find_components(br_mask, image, min_size=1000, print_log=True)

   Apply morphological cleanup, label connected components, filter by size.

   **Parameters:**

   - ``br_mask`` (np.ndarray): Binary mask from b_roth
   - ``image`` (np.ndarray): Corresponding cropped image
   - ``min_size`` (int, optional): Minimum component area in pixels. Default 1000.
   - ``print_log`` (bool, optional): Display results. Default True.

   **Returns:**

   - tuple: (labeled_image, num_components, large_components_mask, component_sizes, bound_box)

   **Example:**

   .. code-block:: python

      labeled, n, large, sizes, bbox = suryapy.find_components(br_mask, cropped)

.. py:function:: inspect_component(target_label, labeled_image, num_components, bound_box, br_mask, image, print_log=True)

   Get detailed info about one labeled component.

   **Parameters:**

   - ``target_label`` (int): Component label (1-based)
   - ``labeled_image`` (np.ndarray): Output of scp.label
   - Other parameters: From find_components output

   **Returns:**

   - dict: With keys ``label``, ``y_start``, ``y_end``, ``x_start``, ``x_end``, ``height``, ``width``, ``area_pixels``

   **Example:**

   .. code-block:: python

      info = suryapy.inspect_component(1, labeled, n, bbox, br, cropped)
      print(f"Area: {info['area_pixels']} pixels")

.. py:function:: foreshortening_correction(area_pixels, y, z, R_sun=1511)

   Correct sunspot area for foreshortening (projection angle).

   .. math::
      A_{\text{corr}} = \frac{A_{\text{obs}}}{\sqrt{1 - (y/R)^2 - (z/R)^2}}

   **Parameters:**

   - ``area_pixels`` (float): Observed area in pixels
   - ``y`` (float): y-coordinate (solar-radius pixels)
   - ``z`` (float): z-coordinate (solar-radius pixels)
   - ``R_sun`` (float, optional): Solar radius in pixels. Default 1511.

   **Returns:**

   - float: Corrected area in pixels

   **Example:**

   .. code-block:: python

      corrected = suryapy.foreshortening_correction(1276, y=-700, z=-900)

.. py:function:: pixels_to_km2(area_pixels, km_per_pixel)

   Convert area in pixels to km².

   **Parameters:**

   - ``area_pixels`` (float): Area in pixels
   - ``km_per_pixel`` (float): Scale (e.g., 458.58 for DSLR internship data)

   **Returns:**

   - float: Area in km²

   **Example:**

   .. code-block:: python

      area_km2 = suryapy.pixels_to_km2(1276, km_per_pixel=458.58)

.. py:function:: km2_to_millionths(area_km2, R_sun_km=696000)

   Convert km² to millionths of solar hemisphere (MH).

   **Parameters:**

   - ``area_km2`` (float): Area in km²
   - ``R_sun_km`` (float, optional): Solar radius in km. Default 696,000.

   **Returns:**

   - float: Area in MH (standard solar physics unit)

   **Example:**

   .. code-block:: python

      area_mh = suryapy.km2_to_millionths(area_km2)
      print(f"Area: {area_mh:.2f} MH")

.. py:function:: angular_distance(x_spot, y_spot, pixel_radius=1516, angular_radius_deg=0.27, x_center=0, y_center=0)

   Compute angular distance of a spot from disk center.

   **Parameters:**

   - ``x_spot``, ``y_spot`` (float): Spot coordinates (solar-radius pixels)
   - ``pixel_radius`` (float, optional): Solar disk radius in pixels. Default 1516.
   - ``angular_radius_deg`` (float, optional): Angular radius in degrees. Default 0.27.

   **Returns:**

   - float: Angular distance in degrees

   **Example:**

   .. code-block:: python

      ang_dist = suryapy.angular_distance(0, 1000)

Summary Table
-------------

.. list-table::
   :header-rows: 1

   * - Function
     - Purpose
     - Input
     - Output

   * - ``b_roth``
     - Adaptive threshold
     - Image
     - Binary mask

   * - ``mask_sun``
     - Isolate and crop sun
     - Image
     - Cropped image

   * - ``find_spot``
     - Locate centroid
     - Image, approx pos
     - (x, y) centroid

   * - ``process``
     - Mask + find spot
     - Image, approx pos
     - (cropped, centroid)

   * - ``limb_darkening_correction``
     - Remove edge darkening
     - Image
     - Corrected image

   * - ``find_components``
     - Label sunspots
     - Mask, image
     - Labeled image, stats

   * - ``inspect_component``
     - Get component info
     - Labels, component ID
     - Dictionary of properties

   * - ``foreshortening_correction``
     - Correct for angle
     - Area, position
     - Corrected area

   * - ``pixels_to_km2``
     - Unit conversion
     - Area (px), calibration
     - Area (km²)

   * - ``km2_to_millionths``
     - Unit conversion
     - Area (km²)
     - Area (MH)

   * - ``angular_distance``
     - Spot location
     - Position, calibration
     - Angular distance (deg)
