Tutorials
=========

In-depth guides for using Sunspots effectively.

Tutorial 1: Understanding Bradley-Roth Thresholding
----------------------------------------------------

The Bradley-Roth algorithm is the core of Sunspots. This tutorial explains how it works.

**What is Adaptive Thresholding?**

Traditional global thresholding uses a single threshold value for the entire image. This fails when lighting varies across the image. Adaptive thresholding computes a threshold locally for each pixel region, making it robust to varying conditions - perfect for solar images.

**The Bradley-Roth Algorithm**

The algorithm works in these steps:

1. Compute the **integral image** (cumulative sum of pixels)
2. For each pixel, define a rectangular neighborhood
3. Use the integral image to quickly compute the **mean** of that neighborhood
4. Compare the pixel value to (mean - constant)
5. If pixel > (mean - constant), mark as foreground (white, 255)

**Why It's Efficient**

Using integral images, computing the mean takes O(1) time instead of O(n²). This makes it much faster than naive implementations.

**Choosing Parameters**

.. code-block:: python

   import sunspots
   
   # Block size: neighborhood size for mean calculation
   # Larger = more context, smoother results
   # Smaller = more detail, noisier results
   
   # Constant: bias term
   # Larger = more aggressive detection
   # Smaller = more conservative detection
   
   binary = sunspots.bradley_roth_threshold(
       image,
       block_size=51,    # Neighborhood is 51x51 pixels
       constant=10.0     # Subtract 10 from local mean
   )

**Visual Comparison**

.. code-block:: python

   import sunspots
   import matplotlib.pyplot as plt
   
   image = sunspots.load_image("solar.jpg")
   
   fig, axes = plt.subplots(1, 4, figsize=(15, 4))
   
   # Original
   axes[0].imshow(image)
   axes[0].set_title("Original Image")
   
   # Different constant values
   for idx, constant in enumerate([5, 10, 15], 1):
       binary = sunspots.bradley_roth_threshold(image, constant=constant)
       axes[idx].imshow(binary, cmap='gray')
       axes[idx].set_title(f"Constant={constant}")
   
   plt.tight_layout()
   plt.show()

Tutorial 2: Image Preprocessing Strategy
-----------------------------------------

Good preprocessing significantly improves detection accuracy.

**The Standard Pipeline**

.. code-block:: python

   import sunspots
   
   # 1. Load
   image = sunspots.load_image("solar.jpg")
   
   # 2. Resize (for performance)
   image = sunspots.resize_image(image, scale=0.8)
   
   # 3. Enhance contrast (CLAHE)
   enhanced = sunspots.apply_clahe(image, clip_limit=2.0)
   
   # 4. Reduce noise (Gaussian blur)
   smooth = sunspots.gaussian_blur(enhanced, kernel_size=5, sigma=1.0)
   
   # 5. Normalize intensity
   normalized = sunspots.normalize_image(smooth, method='minmax')
   
   # 6. Threshold
   binary = sunspots.bradley_roth_threshold(normalized, block_size=51)
   
   # 7. Detect
   spots, stats = sunspots.analyze_contours(binary)

**Understanding Each Step**

- **Resize**: Process 50-80% of original size for speed, minimal loss
- **CLAHE**: Locally enhance contrast without over-amplifying noise
- **Gaussian Blur**: Reduce small noise, improve continuity
- **Normalize**: Put all images on same scale
- **Threshold**: Convert to binary for contour detection

**When to Skip Steps**

- Skip Resize: For small images or when precision is critical
- Skip CLAHE: For already high-contrast images
- Skip Blur: For very clear images or when fine details matter
- Skip Normalize: If images are already normalized

Tutorial 3: Debugging Detection Issues
---------------------------------------

**Problem: No sunspots detected**

Diagnostic checklist:

.. code-block:: python

   import sunspots
   import cv2
   import numpy as np
   
   image = sunspots.load_image("solar.jpg")
   
   # Check 1: Is the image loaded?
   print(f"Image shape: {image.shape}")
   print(f"Value range: {image.min()}-{image.max()}")
   cv2.imshow("Original", image)
   
   # Check 2: Are we getting any white pixels?
   binary = sunspots.bradley_roth_threshold(image, constant=10)
   white_pixels = np.sum(binary > 127)
   print(f"White pixels: {white_pixels}")
   cv2.imshow("Threshold", binary)
   
   # Check 3: Do we have contours?
   contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, 
                                   cv2.CHAIN_APPROX_SIMPLE)
   print(f"Contours found: {len(contours)}")
   
   # Check 4: Are contours being filtered out?
   for area in sorted([cv2.contourArea(c) for c in contours])[-5:]:
       print(f"Contour area: {area}")

**Solution Steps**

1. Increase `constant` parameter (more aggressive)
2. Try larger `block_size` (51, 71, 101)
3. Add preprocessing (CLAHE, normalize)
4. Decrease `min_area` threshold
5. Check image quality - is it clear?

**Problem: Too many false positives**

.. code-block:: python

   # Solution 1: Increase min_area
   spots = sunspots.detect_sunspots(image, min_area=100)
   
   # Solution 2: Decrease constant (less aggressive)
   binary = sunspots.bradley_roth_threshold(image, constant=5)
   
   # Solution 3: Filter by shape
   round_spots = [s for s in spots if s.circularity > 0.6]
   
   # Solution 4: Apply morphological operations
   import cv2
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
   binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

Tutorial 4: Accuracy Assessment
-------------------------------

How to evaluate detection accuracy:

.. code-block:: python

   import sunspots
   
   # Manual ground truth (from visual inspection)
   ground_truth = {
       "count": 8,
       "areas": [500, 650, 750, 1200, 450, 600, 700, 900]
   }
   
   # Automated detection
   image = sunspots.load_image("solar.jpg")
   spots, stats = sunspots.analyze_contours(image)
   
   # Calculate metrics
   detection_rate = (stats['count'] / ground_truth["count"]) * 100
   print(f"Detection rate: {detection_rate:.1f}%")
   
   # Area prediction
   predicted_total = stats['total_area']
   ground_total = sum(ground_truth['areas'])
   area_error = abs(predicted_total - ground_total) / ground_total * 100
   print(f"Area error: {area_error:.1f}%")

Tutorial 5: Production Deployment
---------------------------------

Best practices for production use:

.. code-block:: python

   import sunspots
   import logging
   from pathlib import Path
   
   # Setup logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   def process_solar_image(image_path: str) -> dict:
       """Production-ready sunspot detection function."""
       
       try:
           # Load with error handling
           if not Path(image_path).exists():
               raise FileNotFoundError(f"Image not found: {image_path}")
           
           logger.info(f"Processing {image_path}")
           image = sunspots.load_image(image_path)
           
           # Preprocess
           enhanced = sunspots.apply_clahe(image)
           normalized = sunspots.normalize_image(enhanced)
           
           # Detect
           spots, stats = sunspots.analyze_contours(normalized, min_area=50)
           
           # Validate results
           if stats['count'] < 1:
               logger.warning(f"No sunspots detected in {image_path}")
           else:
               logger.info(f"Detected {stats['count']} sunspots")
           
           return {
               "success": True,
               "image_path": image_path,
               "sunspots_count": stats['count'],
               "total_area": stats['total_area'],
               "statistics": stats
           }
           
       except Exception as e:
           logger.error(f"Error processing {image_path}: {e}")
           return {
               "success": False,
               "image_path": image_path,
               "error": str(e)
           }
   
   # Usage
   results = []
   for image_file in Path("solar_images").glob("*.jpg"):
       result = process_solar_image(str(image_file))
       results.append(result)

Next Steps
----------

- Experiment with your own images
- Try different parameter combinations
- Join our community on GitHub
- Read the :doc:`api_reference` for all available functions
