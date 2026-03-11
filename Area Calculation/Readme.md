# Sunspots Area Calculation 
The following repository contains data as well as python notebook along with functions that can be used to calculate sunspot areas from white light images. Images are from the Royal University of Belgium.
All instructions to use the code is provided in the code file. This project was an extension of my summer internship where we tried to measure the rotation periods of the sunspots.
Please download the ZIP file for the python code, refer to the PDF attached for an in depth discussion of my Analysis and work

## Analysis Overview

This project implements a digital image–processing pipeline to identify sunspots
in solar disk images and estimate their physical areas. The main steps of the
analysis are outlined below.

### 1. Input Solar Images
White-light solar images are used as input. Images may come from ground-based
observations (DSLR + telescope) or public solar databases. Images are assumed
to contain the full solar disk.

### 2. Limb Darkening Correction
The solar disk intensity decreases toward the limb, which affects threshold-based
spot detection. To correct for this:
- A radial intensity profile is constructed by sampling concentric rings.
- The profile is fitted with a smooth polynomial.
- Each pixel is normalized by the fitted radial intensity to obtain a flattened
  (limb-darkening–corrected) image.

### 3. Adaptive Thresholding
The normalized image is converted to a binary image using adaptive thresholding.
This highlights dark regions corresponding to sunspots while accounting for
local intensity variations.

### 4. Morphological Processing
Morphological opening and closing operations are applied to:
- Reduce small-scale noise
- Smooth spot boundaries
- Preserve the overall shape of sunspot regions

### 5. Connected Component Analysis
Connected components are identified in the binary image.
- Each connected region is treated as a candidate sunspot.
- Small components below a chosen area threshold are discarded as noise.

### 6. Area Measurement
The area of each detected sunspot is measured in pixel units using the connected
components.

### 7. Foreshortening Correction
To account for projection effects on the solar disk:
- The heliocentric angle of each sunspot is calculated from its position.
- Observed areas are corrected for foreshortening using geometric factors.

### 8. Conversion to Physical Units
Corrected areas are converted from pixels to physical units, such as:
- square kilometers
- millionths of the solar hemisphere (MH)

### 9. Comparison with Reference Data
Measured sunspot areas are compared with published values from external sources
(e.g., SIDC / SpaceWeatherLive) to assess consistency and accuracy.
