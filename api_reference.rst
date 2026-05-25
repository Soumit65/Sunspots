API Reference
=============

This is the complete API reference for Sunspots.

Thresholding Module
-------------------

.. py:module:: sunspots.thresholding

.. py:function:: bradley_roth_threshold(image, block_size=50, constant=10.0, convert_grayscale=True)

   Apply Bradley-Roth adaptive thresholding to an image.
   
   The Bradley-Roth algorithm compares each pixel to the mean of a rectangular
   neighborhood, making it robust to lighting variations. This is particularly
   effective for sunspot detection.

   **Parameters:**
   
   - ``image`` (np.ndarray): Input image (grayscale or color)
   - ``block_size`` (int): Size of the neighborhood region (must be odd, ≥3)
   - ``constant`` (float): Constant subtracted from the mean ([-255, 255])
   - ``convert_grayscale`` (bool): Convert color images to grayscale
   
   **Returns:**
   
   - np.ndarray: Binary image (values 0 or 255)
   
   **Raises:**
   
   - ValueError: If block_size is even or less than 3
   
   **Example:**
   
   .. code-block:: python
   
      import sunspots
      image = sunspots.load_image("solar.jpg")
      binary = sunspots.bradley_roth_threshold(image, block_size=51, constant=10)

.. py:function:: adaptive_threshold(image, method='bradley', block_size=50, constant=10.0, **kwargs)

   Apply adaptive thresholding using various methods.

   **Parameters:**
   
   - ``image`` (np.ndarray): Input image
   - ``method`` (str): One of 'bradley', 'gaussian', or 'mean'
   - ``block_size`` (int): Neighborhood size
   - ``constant`` (float): Constant value for the method
   
   **Returns:**
   
   - np.ndarray: Binary image
   
   **Example:**
   
   .. code-block:: python
   
      # Using Gaussian method
      binary = sunspots.adaptive_threshold(image, method='gaussian', block_size=51)

Area Calculation Module
-----------------------

.. py:module:: sunspots.area_calculator

.. py:class:: Sunspot

   Data class representing a detected sunspot.
   
   **Attributes:**
   
   - ``area`` (float): Area in pixels
   - ``perimeter`` (float): Perimeter length
   - ``centroid`` (Tuple[float, float]): Center coordinates (x, y)
   - ``bounding_box`` (Tuple[int, int, int, int]): (x, y, width, height)
   - ``contour`` (np.ndarray): OpenCV contour array
   - ``circularity`` (float): Shape measure (4π * area / perimeter²)
   - ``aspect_ratio`` (float): Width/height ratio
   
   **Methods:**
   
   .. py:method:: to_dict()
   
      Convert sunspot properties to a dictionary.
      
      **Returns:**
      
      - dict: Dictionary representation

.. py:function:: detect_sunspots(image, min_area=50.0, max_area=None, threshold_method='otsu')

   Detect sunspots in a solar image.

   **Parameters:**
   
   - ``image`` (np.ndarray): Input image (grayscale or color)
   - ``min_area`` (float): Minimum area threshold for detection
   - ``max_area`` (float): Maximum area threshold (None = no limit)
   - ``threshold_method`` (str): 'otsu' or 'binary'
   
   **Returns:**
   
   - List[Sunspot]: List of detected sunspots
   
   **Example:**
   
   .. code-block:: python
   
      image = sunspots.load_image("solar.jpg")
      spots = sunspots.detect_sunspots(image, min_area=50)
      
      for spot in spots:
          print(f"Area: {spot.area}")
          print(f"Circularity: {spot.circularity}")

.. py:function:: calculate_area(binary_image, pixel_to_mm=1.0)

   Calculate total area of all white regions in a binary image.

   **Parameters:**
   
   - ``binary_image`` (np.ndarray): Binary image (0 or 255)
   - ``pixel_to_mm`` (float): Conversion factor from pixels to real units
   
   **Returns:**
   
   - float: Total area in specified units
   
   **Example:**
   
   .. code-block:: python
   
      total_area = sunspots.calculate_area(binary_image, pixel_to_mm=0.1)

.. py:function:: analyze_contours(image, min_area=50.0, max_area=None)

   Analyze contours in a binary image and return statistics.

   **Parameters:**
   
   - ``image`` (np.ndarray): Binary input image
   - ``min_area`` (float): Minimum area filter
   - ``max_area`` (float): Maximum area filter
   
   **Returns:**
   
   - Tuple[List[Sunspot], dict]: List of sunspots and statistics dictionary
   
   **Statistics Dictionary Contains:**
   
   - ``count``: Number of sunspots detected
   - ``total_area``: Sum of all areas
   - ``mean_area``: Average area
   - ``std_area``: Standard deviation of areas
   - ``min_area``, ``max_area``: Min/max areas
   - ``mean_circularity``: Average circularity
   - ``mean_aspect_ratio``: Average aspect ratio
   
   **Example:**
   
   .. code-block:: python
   
      spots, stats = sunspots.analyze_contours(binary_image)
      print(f"Found {stats['count']} sunspots")
      print(f"Total area: {stats['total_area']:.2f}")

.. py:function:: draw_sunspots(image, sunspots, color=(0, 255, 0), thickness=2)

   Draw detected sunspots on an image.

   **Parameters:**
   
   - ``image`` (np.ndarray): Input image
   - ``sunspots`` (List[Sunspot]): List of sunspots to draw
   - ``color`` (Tuple[int, int, int]): BGR color
   - ``thickness`` (int): Line thickness in pixels
   
   **Returns:**
   
   - np.ndarray: Image with drawn sunspots
   
   **Example:**
   
   .. code-block:: python
   
      result = sunspots.draw_sunspots(image, spots, color=(0, 255, 0))

Utilities Module
----------------

.. py:module:: sunspots.utils

.. py:function:: load_image(path, as_grayscale=False)

   Load an image from disk.

   **Parameters:**
   
   - ``path`` (str): Path to image file
   - ``as_grayscale`` (bool): Load as grayscale
   
   **Returns:**
   
   - np.ndarray: Image array
   
   **Raises:**
   
   - FileNotFoundError: If image not found

.. py:function:: save_image(path, image)

   Save an image to disk.

   **Parameters:**
   
   - ``path`` (str): Output file path
   - ``image`` (np.ndarray): Image to save
   
   **Returns:**
   
   - bool: True if successful

.. py:function:: normalize_image(image, method='minmax')

   Normalize image intensity values.

   **Parameters:**
   
   - ``image`` (np.ndarray): Input image
   - ``method`` (str): 'minmax', 'zscore', or 'histogram'
   
   **Returns:**
   
   - np.ndarray: Normalized image

.. py:function:: resize_image(image, width=None, height=None, scale=None)

   Resize an image while maintaining aspect ratio.

   **Parameters:**
   
   - ``image`` (np.ndarray): Input image
   - ``width`` (int): Target width
   - ``height`` (int): Target height
   - ``scale`` (float): Scale factor (0-1)
   
   **Returns:**
   
   - np.ndarray: Resized image

.. py:function:: apply_clahe(image, clip_limit=2.0, tile_size=8)

   Apply Contrast Limited Adaptive Histogram Equalization.

   **Parameters:**
   
   - ``image`` (np.ndarray): Input image
   - ``clip_limit`` (float): Contrast limit
   - ``tile_size`` (int): Tile grid size
   
   **Returns:**
   
   - np.ndarray: Enhanced image
   
   **Example:**
   
   .. code-block:: python
   
      enhanced = sunspots.apply_clahe(image, clip_limit=2.0)

.. py:function:: gaussian_blur(image, kernel_size=5, sigma=1.0)

   Apply Gaussian blur to reduce noise.

   **Parameters:**
   
   - ``image`` (np.ndarray): Input image
   - ``kernel_size`` (int): Kernel size (must be odd)
   - ``sigma`` (float): Standard deviation
   
   **Returns:**
   
   - np.ndarray: Blurred image

Package-level Imports
---------------------

All main functions are available at the package level:

.. code-block:: python

   import sunspots
   
   # All of these work:
   sunspots.load_image("file.jpg")
   sunspots.bradley_roth_threshold(image)
   sunspots.detect_sunspots(image)
   sunspots.apply_clahe(image)

Version Information
-------------------

.. code-block:: python

   import sunspots
   print(sunspots.__version__)      # Current version
   print(sunspots.__author__)       # Author name
   print(sunspots.__license__)      # License type

Constants and Types
-------------------

All main functions accept:

- **Input**: ``numpy.ndarray`` (standard array type)
- **Output**: ``numpy.ndarray`` (typically uint8 for images)
- **Coordinates**: Tuples (x, y) following OpenCV convention
- **Colors**: BGR tuples for OpenCV (0, 255, 0) = green

Performance Notes
-----------------

**Computation Time (approximate, on CPU)**

- Loading image: < 1s
- Bradley-Roth thresholding (1024×1024): 2-5s
- Contour detection: < 1s
- Total pipeline: 5-10s per image

**Memory Usage**

- ~3 bytes per pixel for RGB
- ~1 byte per pixel for grayscale
- Large arrays may require > 1GB RAM

See Also
--------

- :doc:`getting_started` for usage examples
- :doc:`tutorials` for detailed guides
- :doc:`examples` for complete code samples
