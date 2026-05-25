FAQ
===

Frequently asked questions about Sunspots.

General Questions
-----------------

**Q: What is Sunspots?**

A: Sunspots is a Python package for detecting, tracking, and analyzing sunspots from solar images. It uses the Bradley-Roth adaptive thresholding algorithm along with contour analysis to identify and measure sunspots.

**Q: Who should use Sunspots?**

A: Sunspots is designed for:
   - Solar researchers and astronomers
   - Students studying solar physics
   - Hobbyist solar observers
   - Anyone interested in image processing and computer vision

**Q: Is Sunspots free?**

A: Yes! Sunspots is open source under the MIT license, completely free to use, modify, and distribute.

**Q: How accurate is Sunspots?**

A: Accuracy depends on:
   - Image quality and resolution
   - Parameter tuning for your specific images
   - Solar image preparation
   
   Typical accuracy: 85-95% detection rate with proper parameters.

**Q: Can I use Sunspots for non-sunspot images?**

A: Yes! The algorithms are general-purpose and work well for any dark object on light background. Users have applied it to:
   - Spot detection in medical imaging
   - Defect detection in manufactured parts
   - Cell counting in biology

Installation Questions
----------------------

**Q: What Python version do I need?**

A: Python 3.8 or higher. We recommend Python 3.10 or 3.11.

**Q: Can I install Sunspots on Windows/Mac/Linux?**

A: Yes, Sunspots works on all platforms. Installation is identical across platforms.

**Q: What if I get OpenCV errors?**

A: OpenCV might have platform-specific issues:

.. code-block:: bash

   # Try reinstalling
   pip install --force-reinstall opencv-python
   
   # Or use a pre-built wheel
   pip install opencv-contrib-python

**Q: Do I need a GPU?**

A: No, Sunspots works fine on CPU. GPU acceleration is optional for faster processing of large batches.

**Q: Can I use Sunspots in a virtual environment?**

A: Absolutely! It's recommended:

.. code-block:: bash

   python -m venv sunspots_env
   source sunspots_env/bin/activate  # Linux/Mac
   pip install sunspots

Usage Questions
---------------

**Q: How do I know what block_size to use?**

A: Start with 51 and adjust based on sunspot size:
   - Smaller sunspots: 31-51
   - Medium sunspots: 51-71
   - Large sunspots: 71-101
   
Block size must be odd (31, 51, 71, etc.)

**Q: What constant value should I use?**

A: Start with 10.0 and adjust based on results:
   - More sunspots detected: increase constant (15, 20)
   - Too many false positives: decrease constant (5, 7)

**Q: How do I handle images of different sizes?**

A: Use the resize function:

.. code-block:: python

   import sunspots
   
   image = sunspots.load_image("image.jpg")
   resized = sunspots.resize_image(image, scale=0.5)  # 50% size
   
   # Or specify exact dimensions
   resized = sunspots.resize_image(image, width=512, height=512)

**Q: Can I process images in batches?**

A: Yes! Use a loop:

.. code-block:: python

   import sunspots
   from pathlib import Path
   
   for image_path in Path("images").glob("*.jpg"):
       image = sunspots.load_image(str(image_path))
       spots, stats = sunspots.analyze_contours(image)
       print(f"{image_path}: {stats['count']} sunspots")

**Q: How do I save results?**

A: Multiple ways:

.. code-block:: python

   import sunspots
   import csv
   
   image = sunspots.load_image("solar.jpg")
   spots, stats = sunspots.analyze_contours(image)
   
   # Save visualization
   result = sunspots.draw_sunspots(image, spots)
   sunspots.save_image("result.jpg", result)
   
   # Save to CSV
   with open("results.csv", "w") as f:
       writer = csv.writer(f)
       for spot in spots:
           writer.writerow([spot.area, spot.circularity])

**Q: What does circularity mean?**

A: Circularity measures how circular an object is:
   - 1.0 = perfect circle
   - 0.7-0.9 = fairly round
   - < 0.7 = irregular shape
   
Formula: circularity = 4π × area / perimeter²

**Q: How do I filter results by properties?**

A: Use Python list comprehensions:

.. code-block:: python

   # Only round sunspots
   round_spots = [s for s in spots if s.circularity > 0.7]
   
   # Medium-sized sunspots
   medium = [s for s in spots if 500 < s.area < 5000]
   
   # Sunspots in a region
   region_spots = [s for s in spots if 100 < s.centroid[0] < 400]

Performance Questions
---------------------

**Q: How fast is Sunspots?**

A: Approximate timings (1024×1024 image on CPU):
   - Loading: 0.1s
   - Preprocessing: 0.5s
   - Thresholding: 2-5s
   - Detection: 0.5-1s
   - Total: 3-8 seconds

**Q: Can I speed it up?**

A: Yes:

.. code-block:: python

   # 1. Resize image
   image = sunspots.resize_image(image, scale=0.5)  # 4x faster
   
   # 2. Use smaller block size (if acceptable)
   binary = sunspots.bradley_roth_threshold(image, block_size=31)
   
   # 3. Skip unnecessary preprocessing
   
   # 4. Use GPU OpenCV (advanced)

**Q: Does Sunspots support GPU?**

A: OpenCV can be compiled with GPU support. The current version uses CPU. GPU support is on the roadmap.

Troubleshooting
---------------

**Q: I'm getting "ModuleNotFoundError: No module named 'sunspots'"**

A: Sunspots isn't installed. Run:

.. code-block:: bash

   pip install sunspots

Or from source:

.. code-block:: bash

   git clone https://github.com/Soumit65/Sunspots.git
   cd Sunspots
   pip install -e .

**Q: "ImportError: DLL load failed" on Windows**

A: Install Visual C++ redistributable:
   https://support.microsoft.com/en-us/help/2977003/

**Q: No sunspots detected in my images**

A: Try:
   1. Increase `constant` parameter (10 → 15 → 20)
   2. Increase `block_size` (51 → 71 → 101)
   3. Add preprocessing (apply_clahe, normalize)
   4. Decrease `min_area` threshold

**Q: Too many false positives**

A: Try:
   1. Increase `min_area`
   2. Decrease `constant`
   3. Increase `block_size`
   4. Filter by circularity (> 0.6)

**Q: Memory error with large images**

A: Resize images:

.. code-block:: python

   image = sunspots.resize_image(image, scale=0.5)

**Q: Processing is very slow**

A: Try:
   1. Resize images
   2. Skip unnecessary preprocessing
   3. Use smaller block_size
   4. Process in parallel (multiprocessing)

Contributing Questions
----------------------

**Q: How can I contribute?**

A: We welcome contributions! 

1. Fork the repository
2. Create a branch for your feature
3. Make changes
4. Submit a pull request

See our GitHub repository for details.

**Q: How can I report bugs?**

A: Please use the GitHub Issues tracker:
   https://github.com/Soumit65/Sunspots/issues

Include:
   - Your Python version
   - Sunspots version
   - Error message
   - Minimal code to reproduce

**Q: How can I request features?**

A: Open a GitHub Discussion or Issue with your idea. We'd love to hear suggestions!

**Q: Can I use Sunspots in commercial applications?**

A: Yes! The MIT license allows commercial use. You only need to include the license text.

Research Questions
------------------

**Q: Can I cite Sunspots in my research?**

A: Yes! Use this citation:

.. code-block:: bibtex

   @software{sunspots2024,
     author = {Dey, Soumit},
     title = {Sunspots: Sunspot Detection and Analysis Package},
     year = {2024},
     url = {https://github.com/Soumit65/Sunspots}
   }

**Q: Is there a paper describing the algorithm?**

A: The Bradley-Roth algorithm is described in:

   Bradley, D., & Roth, G. (2007). Adaptive Thresholding using the Integral Image. Journal of Graphics Tools, 12(2), 13-21.

**Q: How does Sunspots compare to other tools?**

A: Sunspots is:
   - **Simpler**: Easier to use than manual analysis
   - **Faster**: Processing many images quickly
   - **Open source**: Free and customizable
   - **Specialized**: Designed for sunspot detection specifically

Can't Find Your Question?
-------------------------

Check:
- :doc:`getting_started` for basic usage
- :doc:`api_reference` for function documentation
- :doc:`tutorials` for detailed guides
- :doc:`examples` for code samples
- GitHub Issues: https://github.com/Soumit65/Sunspots/issues

Still need help? Open an issue on GitHub!
