Getting Started
===============

Welcome to Sunspots! This guide will help you get up and running in minutes.

What is Sunspots?
-----------------

Sunspots is a Python package for analyzing solar images, specifically designed to:

- Detect sunspots automatically
- Calculate their areas and properties
- Track them across multiple images
- Provide detailed measurements (circularity, aspect ratio, etc.)

Core Concepts
-------------

**Binary Image**: A black and white image where sunspots appear as white regions.

**Adaptive Thresholding**: A technique that converts grayscale images to binary based on local neighborhood statistics, making it robust to varying lighting conditions.

**Contour Analysis**: The process of finding and analyzing the boundaries of objects (sunspots) in binary images.

**Bradley-Roth Algorithm**: An efficient adaptive thresholding method that uses integral images for fast computation.

Basic Workflow
--------------

The typical workflow for sunspot analysis is:

1. **Load Image**: Read a solar image file
2. **Preprocess**: Optional enhancement (CLAHE, blur, normalize)
3. **Threshold**: Convert to binary image
4. **Detect**: Find sunspots using contour analysis
5. **Analyze**: Calculate properties and statistics
6. **Visualize**: Draw results and save

Example: Complete Analysis
---------------------------

Here's a complete example:

.. code-block:: python

   import sunspots
   from sunspots import (
       load_image, 
       bradley_roth_threshold,
       detect_sunspots,
       analyze_contours,
       draw_sunspots,
       apply_clahe
   )
   import cv2

   # Step 1: Load image
   image = load_image("solar_image.jpg")
   
   # Step 2: Preprocess (optional but recommended)
   enhanced = apply_clahe(image, clip_limit=2.0)
   
   # Step 3: Apply adaptive thresholding
   binary = bradley_roth_threshold(enhanced, block_size=51, constant=10)
   
   # Step 4: Detect sunspots
   sunspots_list, stats = analyze_contours(binary, min_area=50)
   
   # Step 5: Analyze results
   print(f"Found {stats['count']} sunspots")
   print(f"Total area: {stats['total_area']:.2f} pixels")
   print(f"Mean circularity: {stats['mean_circularity']:.3f}")
   
   # Step 6: Visualize
   result = draw_sunspots(image, sunspots_list)
   cv2.imwrite("result.jpg", result)

Key Parameters to Tune
----------------------

**Block Size**: Controls the size of the neighborhood for thresholding.
   - Larger values (51-101): Better for large sunspots
   - Smaller values (31-51): Better for small details
   - Must be odd numbers

**Constant**: Adjusted subtracted from the mean.
   - Higher values (10-15): More aggressive detection
   - Lower values (5-10): More conservative detection
   - Depends on image contrast

**Min Area**: Minimum sunspot size to detect (in pixels).
   - Filters out noise and very small features
   - Typical range: 20-100

Common Issues and Solutions
----------------------------

**Problem: No sunspots detected**
   - Try adjusting the constant value (increase it)
   - Check if image is properly loaded
   - Verify block_size is appropriate for your image

**Problem: Too many false positives**
   - Increase min_area parameter
   - Decrease the constant value
   - Apply preprocessing (CLAHE, blur) first

**Problem: Slow processing**
   - Reduce image size with resize_image()
   - Use smaller block_size if feasible
   - Consider GPU acceleration for OpenCV

Performance Tips
----------------

1. **Preprocess wisely**: CLAHE enhancement can significantly improve detection
2. **Resize if needed**: Processing smaller images is faster
3. **Filter appropriately**: Use min_area to eliminate noise
4. **Batch processing**: Process multiple images in loops

Next Steps
----------

- See :doc:`installation` for detailed setup instructions
- Check :doc:`api_reference` for all available functions
- Explore :doc:`examples` for more complex use cases
- Read :doc:`tutorials` for in-depth guides
