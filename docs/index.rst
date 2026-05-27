SuryaPy
========

A lightweight Python package for detecting and analysing sunspots from solar images using adaptive thresholding and connected-component analysis.

Developed during the Astro Lab Summer Internship 2024.

.. image:: images/suryapy_pipeline.png
   :width: 400px
   :align: center

Image taken from SIDC Royal Observatory of Belgium: https://www.sidc.be/

Features
--------

- Solar disc masking and cropping
- Bradley–Roth adaptive thresholding
- Connected-component analysis
- Sunspot area estimation
- Foreshortening corrections
- Tracking utilities for solar observations

Installation
------------

.. code-block:: bash

   pip install suryapy==0.1.0

Quick Example
-------------

.. code-block:: python

   from suryapy import mask_sun, b_roth

   cropped = mask_sun(image)
   thresholded = b_roth(cropped, threshold=10)

Documentation
-------------

Explore the tutorials and examples to understand the full processing pipeline.
