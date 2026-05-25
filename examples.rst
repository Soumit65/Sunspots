Examples
========

This page contains practical examples of using Sunspots for various tasks.

Example 1: Basic Sunspot Detection
----------------------------------

Simple script to detect sunspots in a single image:

.. code-block:: python

   import sunspots
   import cv2

   # Load image
   image = sunspots.load_image("solar_image.jpg")

   # Detect sunspots
   sunspots_list, stats = sunspots.analyze_contours(image, min_area=50)

   # Print results
   print(f"Detected {stats['count']} sunspots")
   print(f"Total area: {stats['total_area']:.2f} pixels")
   print(f"Average area: {stats['mean_area']:.2f} pixels")

   # Visualize
   result = sunspots.draw_sunspots(image, sunspots_list)
   cv2.imshow("Detection Result", result)
   cv2.waitKey(0)

Example 2: Batch Processing Multiple Images
--------------------------------------------

Process multiple solar images and save results:

.. code-block:: python

   import sunspots
   import os
   from pathlib import Path

   input_dir = "solar_images/"
   output_dir = "results/"
   Path(output_dir).mkdir(exist_ok=True)

   results = []

   for filename in os.listdir(input_dir):
       if filename.endswith(".jpg"):
           filepath = os.path.join(input_dir, filename)
           image = sunspots.load_image(filepath)
           
           # Detect sunspots
           spots, stats = sunspots.analyze_contours(image, min_area=50)
           
           # Save results
           result_image = sunspots.draw_sunspots(image, spots)
           output_path = os.path.join(output_dir, f"result_{filename}")
           sunspots.save_image(output_path, result_image)
           
           # Record statistics
           results.append({
               "image": filename,
               "count": stats['count'],
               "total_area": stats['total_area'],
               "mean_area": stats['mean_area']
           })

   # Print summary
   for r in results:
       print(f"{r['image']}: {r['count']} sunspots, area {r['total_area']:.2f}")

Example 3: Parameter Tuning
----------------------------

Finding optimal parameters for your images:

.. code-block:: python

   import sunspots
   import cv2

   image = sunspots.load_image("solar_image.jpg")

   # Try different block sizes
   block_sizes = [31, 51, 71, 101]
   constants = [5, 10, 15, 20]

   best_config = None
   best_count = 0

   for block_size in block_sizes:
       for constant in constants:
           # Apply thresholding
           binary = sunspots.bradley_roth_threshold(
               image, 
               block_size=block_size, 
               constant=constant
           )
           
           # Detect sunspots
           spots, stats = sunspots.analyze_contours(binary)
           
           print(f"block_size={block_size}, constant={constant}: "
                 f"{stats['count']} spots")
           
           if stats['count'] > best_count:
               best_count = stats['count']
               best_config = (block_size, constant)

   print(f"\nBest configuration: block_size={best_config[0]}, "
         f"constant={best_config[1]}")

Example 4: Image Enhancement Pipeline
--------------------------------------

Full preprocessing pipeline for improved detection:

.. code-block:: python

   import sunspots

   image = sunspots.load_image("solar_image.jpg")

   # Step 1: Resize if needed (for faster processing)
   image = sunspots.resize_image(image, scale=0.5)

   # Step 2: Apply CLAHE enhancement
   enhanced = sunspots.apply_clahe(image, clip_limit=2.0, tile_size=8)

   # Step 3: Reduce noise with Gaussian blur
   smoothed = sunspots.gaussian_blur(enhanced, kernel_size=5, sigma=1.0)

   # Step 4: Normalize intensity
   normalized = sunspots.normalize_image(smoothed, method='minmax')

   # Step 5: Apply thresholding
   binary = sunspots.bradley_roth_threshold(normalized, block_size=51, constant=10)

   # Step 6: Detect and analyze
   spots, stats = sunspots.analyze_contours(binary)

   print(f"Found {stats['count']} sunspots after preprocessing")

Example 5: Tracking Sunspots Over Time
---------------------------------------

Simple tracking of sunspots across consecutive images:

.. code-block:: python

   import sunspots
   import numpy as np

   image_files = ["solar_20240601.jpg", "solar_20240602.jpg", "solar_20240603.jpg"]
   tracks = []

   for i, filename in enumerate(image_files):
       image = sunspots.load_image(filename)
       spots, stats = sunspots.analyze_contours(image, min_area=50)
       
       for spot in spots:
           centroid = spot.centroid
           area = spot.area
           
           # Try to match with previous frame
           if i > 0:
               matched = False
               for track in tracks:
                   last_pos = track['positions'][-1]
                   distance = np.sqrt((centroid[0] - last_pos[0])**2 + 
                                     (centroid[1] - last_pos[1])**2)
                   
                   # If close enough, add to existing track
                   if distance < 50:
                       track['positions'].append(centroid)
                       track['areas'].append(area)
                       matched = True
                       break
               
               if not matched:
                   # Create new track
                   tracks.append({
                       'start_frame': i,
                       'positions': [centroid],
                       'areas': [area]
                   })
           else:
               # First frame - create new tracks
               tracks.append({
                   'start_frame': 0,
                   'positions': [centroid],
                   'areas': [area]
               })

   # Print tracking results
   for i, track in enumerate(tracks):
       print(f"Track {i}: {len(track['positions'])} frames, "
             f"area change: {track['areas'][0]:.2f} -> {track['areas'][-1]:.2f}")

Example 6: Export Results to CSV
--------------------------------

Export detected sunspots to CSV for further analysis:

.. code-block:: python

   import sunspots
   import csv

   image = sunspots.load_image("solar_image.jpg")
   spots, stats = sunspots.analyze_contours(image)

   # Write to CSV
   with open("sunspots.csv", "w", newline="") as f:
       writer = csv.writer(f)
       writer.writerow(["ID", "Area", "Perimeter", "Circularity", 
                       "Centroid_X", "Centroid_Y", "Aspect_Ratio"])
       
       for i, spot in enumerate(spots, 1):
           writer.writerow([
               i,
               f"{spot.area:.2f}",
               f"{spot.perimeter:.2f}",
               f"{spot.circularity:.3f}",
               f"{spot.centroid[0]:.2f}",
               f"{spot.centroid[1]:.2f}",
               f"{spot.aspect_ratio:.2f}"
           ])

   print(f"Exported {len(spots)} sunspots to sunspots.csv")

Example 7: Creating Custom Visualization
-----------------------------------------

Create a detailed visualization with annotations:

.. code-block:: python

   import sunspots
   import cv2
   import numpy as np

   image = sunspots.load_image("solar_image.jpg")
   spots, stats = sunspots.analyze_contours(image)

   # Create annotated image
   result = image.copy()

   for i, spot in enumerate(spots, 1):
       # Draw contour
       cv2.drawContours(result, [spot.contour], 0, (0, 255, 0), 2)
       
       # Draw centroid
       cx, cy = spot.centroid
       cv2.circle(result, (int(cx), int(cy)), 5, (0, 0, 255), -1)
       
       # Add text annotation
       text = f"#{i}: A={spot.area:.0f}"
       cv2.putText(result, text, (int(cx), int(cy)-20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

   # Add statistics box
   stats_text = f"Total: {stats['count']} | Area: {stats['total_area']:.0f}"
   cv2.putText(result, stats_text, (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

   cv2.imshow("Annotated Result", result)
   cv2.imwrite("annotated_result.jpg", result)

Example 8: Filtering by Properties
-----------------------------------

Detect only sunspots matching specific criteria:

.. code-block:: python

   import sunspots

   image = sunspots.load_image("solar_image.jpg")
   all_spots, _ = sunspots.analyze_contours(image)

   # Filter by circularity (rounder = closer to 1.0)
   round_spots = [s for s in all_spots if s.circularity > 0.7]

   # Filter by aspect ratio (more square)
   square_spots = [s for s in all_spots if 0.8 < s.aspect_ratio < 1.2]

   # Filter by size range
   medium_spots = [s for s in all_spots if 1000 < s.area < 10000]

   print(f"Round spots (circularity > 0.7): {len(round_spots)}")
   print(f"Square spots (0.8 < aspect < 1.2): {len(square_spots)}")
   print(f"Medium spots (1000-10000 px²): {len(medium_spots)}")

Tips and Best Practices
-----------------------

1. **Always preprocess**: CLAHE enhancement often improves results
2. **Tune parameters**: Different images need different settings
3. **Use batch processing**: Process multiple images efficiently
4. **Validate results**: Visually check a sample of detected regions
5. **Store metadata**: Keep track of processing parameters
6. **Use version control**: Track which parameters gave best results

Next Steps
----------

- See :doc:`tutorials` for more detailed guides
- Check :doc:`api_reference` for function documentation
- Visit our `GitHub repository <https://github.com/Soumit65/Sunspots>`_
