Tutorials
=========

Tutorial 1: Understanding Bradley-Roth Thresholding
---------------------------------------------------

**What It Does**

Bradley-Roth converts a grayscale image to binary (0 or 1) using an **adaptive** threshold — each pixel's threshold depends on its local neighborhood, not a global value.

This is powerful because:
- Solar images have gradients (bright center, dimmer edges)
- A global threshold would fail near the limb
- Local thresholds adapt to local lighting

**The Algorithm (4 Steps)**

1. **Compute integral image** — 2D cumulative sum for O(1) window queries

   .. code-block:: python

      int_image = np.cumsum(np.cumsum(image, axis=1), axis=0)

2. **For each pixel**, define a window of size `(width // Nx) × (height // Nx)`

   .. code-block:: python

      s = image.shape[1] // Nx   # window size
      # Windows centered on pixel (y, x)
      y1, y2 = y - s//2, y + s//2
      x1, x2 = x - s//2, x + s//2

3. **Query sum in window using integral image** — O(1)

   .. code-block:: python

      total = int_image[y2, x2] - int_image[y1-1, x2] - int_image[y2, x1-1] + int_image[y1-1, x1-1]
      count = (y2 - y1) * (x2 - x1)
      local_mean = total / count

4. **Compare pixel to threshold**

   .. code-block:: python

      if pixel > local_mean * (100 - threshold) / 100:
          output = 1  # foreground (bright)
      else:
          output = 0  # background (dark, sunspot)

**Tuning `threshold` and `Nx`**

.. code-block:: python

   br = suryapy.b_roth(cropped, threshold=9, Nx=100)

| Parameter | Effect | Typical Range |
|-----------|--------|---------------|
| `threshold` | Sensitivity. Higher = darker pixels marked as foreground | 5–20 |
| `Nx` | Window divisor. Larger Nx = smaller window | 50–150 |

**Example: Playing with Parameters**

.. code-block:: python

   import matplotlib.pyplot as plt
   import suryapy

   fig, axes = plt.subplots(2, 3, figsize=(12, 8))

   thresholds = [5, 9, 15]
   for i, t in enumerate(thresholds):
       br = suryapy.b_roth(cropped, threshold=t, Nx=100, print_log=False)
       axes[0, i].imshow(br, cmap='gray')
       axes[0, i].set_title(f'threshold={t}')

   nxs = [50, 100, 150]
   for i, nx in enumerate(nxs):
       br = suryapy.b_roth(cropped, threshold=9, Nx=nx, print_log=False)
       axes[1, i].imshow(br, cmap='gray')
       axes[1, i].set_title(f'Nx={nx}')

   plt.tight_layout()
   plt.show()

Tutorial 2: Limb Darkening Correction
--------------------------------------

**The Problem**

The sun's intensity decreases toward the edges (limb) because we see the cooler upper layers. A thresholding algorithm will be biased — it might miss faint spots near the limb, or over-detect near the center.

**The Solution**

Compute the radial intensity profile:

1. For each distance r from the image center, measure the median intensity of all pixels at radius r
2. Fit a 3rd-degree polynomial to this profile
3. Divide each pixel by the fitted value at its radius

**Code Walkthrough**

.. code-block:: python

   import numpy as np
   from scipy.optimize import curve_fit
   import suryapy

   # Correct
   corrected = suryapy.limb_darkening_correction(cropped, show_plot=True)

   # What's happening under the hood:
   # 1. Compute radial distances
   h, w = cropped.shape
   center = (h // 2, w // 2)
   y, x = np.indices((h, w))
   radii = np.sqrt((x - center[1])**2 + (y - center[0])**2).astype(int)

   # 2. Median intensity at each radius
   max_r = int(radii.max())
   medians = []
   for r in range(max_r + 1):
       mask = (radii == r)
       if np.any(mask):
           medians.append(np.median(cropped[mask]))
       else:
           medians.append(0)

   # 3. Fit 3rd-degree polynomial
   def poly3(r, a, b, c, d):
       return a*r**3 + b*r**2 + c*r + d

   r_vals = np.arange(max_r + 1)
   params, _ = curve_fit(poly3, r_vals, medians)
   profile = poly3(r_vals, *params)

   # 4. Divide to correct
   corrected = np.zeros_like(cropped, dtype=float)
   for r in range(max_r + 1):
       mask = (radii == r)
       if profile[r] > 0:
           corrected[mask] = cropped[mask] / profile[r]

**When to Use**

- ✅ If you see a brightness gradient (natural)
- ✅ If thresholding is biased toward bright regions
- ❌ If image is already very flat (unlikely with DSLR)

Tutorial 3: Connected Component Analysis
-----------------------------------------

**What We're Doing**

After thresholding, we have a binary mask. Dark pixels = sunspots, bright = background. How do we find individual sunspots?

Answer: Label connected regions (connected components).

**The Pipeline**

1. **Morphological cleanup** — Remove noise

   .. code-block:: python

      from scipy import ndimage as scp
      struct = np.ones((3, 3))
      opened = scp.binary_opening(cropped, structure=struct)  # Remove small bright
      closed = scp.binary_closing(br_mask, structure=struct)  # Fill holes in dark

2. **Isolate sunspots**

   .. code-block:: python

      isolated = closed * cropped * opened

3. **Label connected components**

   .. code-block:: python

      labeled, n = scp.label(isolated == 0)  # 0 = dark = sunspot

4. **Size filter**

   .. code-block:: python

      sizes = np.bincount(labeled.ravel())[1:]  # skip background (label 0)
      large_mask = sizes >= 1000  # keep only large components

5. **Inspect**

   .. code-block:: python

      bbox = scp.find_objects(labeled)
      for i, size in enumerate(sizes):
          if size >= 1000:
              print(f"Component {i+1}: {size} pixels")

**In SuryaPy**

.. code-block:: python

   labeled, n, large_mask, sizes, bbox = suryapy.find_components(
       br_mask, cropped, min_size=1000, print_log=True
   )

Tutorial 4: Foreshortening Correction
--------------------------------------

**The Problem**

A sunspot near the solar limb (edge) is viewed at an angle. Its projected area is smaller than its true area on the solar surface. We need to correct for this projection.

**The Math**

For a spot at heliocentric coordinates (y, z) on a sphere of radius R:

.. math::
   A_{\text{corrected}} = \frac{A_{\text{observed}}}{\sqrt{1 - (y/R)^2 - (z/R)^2}}

**Intuition**

- Spot at center (y=0, z=0): no correction (divide by 1)
- Spot at limb (y²+z² → R²): large correction (denominator → 0)

**Example**

.. code-block:: python

   import suryapy

   # Spot observed as 1276 pixels
   # Located at (y=-700, z=-900) in solar-radius pixel coords
   # Solar radius R = 1511 pixels
   
   corrected = suryapy.foreshortening_correction(
       area_pixels=1276,
       y=-700, z=-900,
       R_sun=1511
   )
   # Result: ~1456 pixels (about 14% larger)

**Coordinates**

- **Image pixel coords**: (0, 0) to (height, width)
- **Solar-radius coords**: (-R, -R) to (+R, +R), origin at disc center

The ``process`` and ``find_spot`` functions return spots in solar-radius coordinates, not image pixels. Use those directly.

Tutorial 5: Physical Units
---------------------------

**Pixels → km²**

Measured pixels depend on your instrument's angular resolution and distance to Sun.

From the internship:
- DSLR: 458.58 km/pixel
- SIDC: 738.44 km/pixel

.. code-block:: python

   km_per_pixel = 458.58  # Your DSLR
   area_km2 = suryapy.pixels_to_km2(area_corrected, km_per_pixel)

**km² → Millionths of Hemisphere (MH)**

Standard unit in solar physics. The solar hemisphere is 2πR_sun²:

.. code-block:: python

   area_mh = suryapy.km2_to_millionths(area_km2)
   # E.g., 350 km² → 90.5 MH

**Angular Distance**

Where on the disk is the spot?

.. code-block:: python

   angular_deg = suryapy.angular_distance(x_spot=0, y_spot=1000, pixel_radius=1516)
