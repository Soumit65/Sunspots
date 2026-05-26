Installation
=============

System Requirements
-------------------

- **Python**: 3.8 or higher
- **pip**: Python package manager
- **astrolab**: Your college's solar imaging library (must be installed)
- **~200 MB** disk space for dependencies

Operating Systems
~~~~~~~~~~~~~~~~~~

SuryaPy works on Linux, macOS, and Windows.

Installation Methods
---------------------

**Option 1: From Source (Recommended)**

Clone and install in editable mode:

.. code-block:: bash

   git clone https://github.com/Soumit65/SuryaPy.git
   cd SuryaPy
   pip install -e .

**Option 2: With Development Tools**

For contributing or building docs:

.. code-block:: bash

   pip install -e ".[dev,docs,jupyter]"

This installs:
- Testing: pytest, pytest-cov
- Code quality: black, flake8, isort, mypy
- Documentation: sphinx, sphinx-rtd-theme
- Jupyter: jupyter, notebook

**Option 3: From PyPI (When Published)**

.. code-block:: bash

   pip install suryapy

Verify Installation
-------------------

Check that SuryaPy is properly installed:

.. code-block:: bash

   python -c "import sunspots; print(sunspots.__version__)"

Output should be: ``0.1.0``

Dependencies
------------

**Required**

- **astrolab** ≥ 0.1.0 — Solar imaging library (your college's)
- **numpy** ≥ 1.19.0 — Numerical arrays
- **scipy** ≥ 1.5.0 — scipy.ndimage for connected components
- **matplotlib** ≥ 3.3.0 — Plotting and display

**Optional**

For development:

.. code-block:: bash

   pip install pytest pytest-cov black flake8 isort mypy

For documentation:

.. code-block:: bash

   pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints

For Jupyter notebooks:

.. code-block:: bash

   pip install jupyter notebook ipykernel

Troubleshooting
---------------

**"ModuleNotFoundError: No module named 'sunspots'"**

Ensure you installed it:

.. code-block:: bash

   cd path/to/SuryaPy
   pip install -e .

Or check your Python path:

.. code-block:: bash

   python -c "import sys; print(sys.path)"

**"ModuleNotFoundError: No module named 'astrolab'"**

Install astrolab from your college's repository:

.. code-block:: bash

   git clone https://github.com/your-college/astrolab.git
   cd astrolab
   pip install -e .

Check the astrolab documentation for setup.

**Import error: "cannot import name 'find_star' from 'astrolab.imaging'"**

Ensure astrolab is properly installed and up-to-date. Check that ``im.find_star`` exists in your astrolab version.

**"ModuleNotFoundError: No module named 'scipy'"**

Install scipy:

.. code-block:: bash

   pip install scipy

**Slow processing**

If installation is slow, upgrade pip, setuptools, and wheel:

.. code-block:: bash

   pip install --upgrade pip setuptools wheel
   pip install -e .

Using Virtual Environments
----------------------------

Recommended to isolate SuryaPy from other projects:

**venv (built-in)**

.. code-block:: bash

   python -m venv suryapy_env
   source suryapy_env/bin/activate  # On Windows: suryapy_env\Scripts\activate
   pip install -e .

**conda**

.. code-block:: bash

   conda create -n suryapy python=3.10
   conda activate suryapy
   pip install -e .

Deactivate when done:

.. code-block:: bash

   deactivate  # or conda deactivate

Building Documentation Locally
-------------------------------

To build the docs yourself:

.. code-block:: bash

   pip install -r requirements-docs.txt
   cd docs
   sphinx-build -b html . _build/html
   open _build/html/index.html

Or on Windows:

.. code-block:: bash

   start _build/html/index.html

Next Steps
----------

After installation:

1. Read :doc:`quick_start` for a 5-minute tutorial
2. Try :doc:`examples` to see real workflows
3. Explore :doc:`api_reference` for all functions
4. Check :doc:`faq` for common questions
