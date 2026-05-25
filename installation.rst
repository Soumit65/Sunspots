Installation
=============

This guide covers multiple ways to install Sunspots.

System Requirements
-------------------

- Python 3.8 or higher
- pip (Python package manager)
- ~500 MB disk space for dependencies

Operating Systems
~~~~~~~~~~~~~~~~~~

Sunspots works on:
- Linux (Ubuntu, Debian, CentOS, etc.)
- macOS (Intel and Apple Silicon)
- Windows (7, 8, 10, 11)

Installation Methods
---------------------

Option 1: Install from PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once Sunspots is published to PyPI, installation is easiest via pip:

.. code-block:: bash

   pip install sunspots

To upgrade an existing installation:

.. code-block:: bash

   pip install --upgrade sunspots

Option 2: Install from Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install directly from the GitHub repository:

.. code-block:: bash

   git clone https://github.com/Soumit65/Sunspots.git
   cd Sunspots
   pip install .

For development (editable install):

.. code-block:: bash

   pip install -e .

Option 3: Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to contribute or modify the package:

.. code-block:: bash

   git clone https://github.com/Soumit65/Sunspots.git
   cd Sunspots
   pip install -e ".[dev,docs]"

This installs:
- Development tools (pytest, black, flake8)
- Documentation dependencies (sphinx, sphinx-rtd-theme)

Verify Installation
-------------------

Check that Sunspots is properly installed:

.. code-block:: bash

   python -c "import sunspots; print(sunspots.__version__)"

Or in Python:

.. code-block:: python

   import sunspots
   print(sunspots.__version__)
   print(dir(sunspots))

Dependencies
------------

Sunspots automatically installs these dependencies:

Core Dependencies
~~~~~~~~~~~~~~~~~

- **numpy** (>=1.19.0): Numerical computing
- **opencv-python** (>=4.5.0): Computer vision library
- **matplotlib** (>=3.3.0): Visualization
- **scipy** (>=1.5.0): Scientific computing
- **scikit-image** (>=0.18.0): Image processing
- **Pillow** (>=8.0.0): Image I/O

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~

For development:

.. code-block:: bash

   pip install pytest pytest-cov black flake8 isort mypy

For documentation:

.. code-block:: bash

   pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints

For Jupyter notebooks:

.. code-block:: bash

   pip install jupyter notebook ipykernel

GPU Acceleration (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For GPU-accelerated OpenCV:

.. code-block:: bash

   # NVIDIA CUDA support
   pip install opencv-contrib-python

   # Then rebuild OpenCV with CUDA support
   # (Instructions vary by system)

Troubleshooting
---------------

Problem: "ModuleNotFoundError: No module named 'sunspots'"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution**: Ensure Sunspots is installed:

.. code-block:: bash

   pip install sunspots

Or if installing from source:

.. code-block:: bash

   cd path/to/Sunspots
   pip install -e .

Problem: "ImportError: DLL load failed" (Windows with OpenCV)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution**: Install Visual C++ redistributable:
   - Download from: https://support.microsoft.com/en-us/help/2977003/
   - Or use: `pip install opencv-python==<version> --force-reinstall`

Problem: Version conflicts with other packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution**: Use a virtual environment:

.. code-block:: bash

   # Create virtual environment
   python -m venv sunspots_env
   
   # Activate it
   source sunspots_env/bin/activate  # Linux/Mac
   # or
   sunspots_env\Scripts\activate  # Windows
   
   # Install Sunspots
   pip install sunspots

Problem: Slow/incomplete installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution**: Upgrade pip, setuptools, and wheel:

.. code-block:: bash

   pip install --upgrade pip setuptools wheel
   pip install sunspots

Virtual Environments (Recommended)
----------------------------------

Using Python's venv:

.. code-block:: bash

   # Create
   python -m venv sunspots_env
   
   # Activate
   source sunspots_env/bin/activate  # Linux/Mac
   sunspots_env\Scripts\activate      # Windows
   
   # Install Sunspots
   pip install sunspots
   
   # Deactivate
   deactivate

Using Conda:

.. code-block:: bash

   # Create
   conda create -n sunspots python=3.10
   
   # Activate
   conda activate sunspots
   
   # Install
   pip install sunspots

Getting Help
------------

If installation fails:

1. Check Python version: `python --version` (should be 3.8+)
2. Upgrade pip: `pip install --upgrade pip`
3. Check internet connection
4. Visit: https://github.com/Soumit65/Sunspots/issues
5. Check OpenCV requirements: https://docs.opencv.org/master/

Next Steps
----------

After installation, see :doc:`getting_started` to begin using Sunspots!
