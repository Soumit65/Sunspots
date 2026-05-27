Installation
=============

SuryaPy can be installed directly from PyPI using ``pip``.

Basic Installation
------------------

.. code-block:: bash

   pip install suryapy

This installs the core package and required scientific Python dependencies.

Requirements
------------

SuryaPy requires:

- Python 3.8+
- NumPy
- SciPy
- Matplotlib
- AstroLab

Installing from Source
----------------------

To install the latest development version directly from GitHub:

.. code-block:: bash

   git clone https://github.com/Soumit65/SuryaPy.git

.. code-block:: bash

   cd SuryaPy

.. code-block:: bash

   pip install -e .

The ``-e`` flag installs the package in editable mode, which is useful for development.

Verifying the Installation
--------------------------

After installation, test the package:

.. code-block:: python

   import suryapy

   print("SuryaPy installed successfully!")

You can also inspect the available functions:

.. code-block:: python

   print(dir(suryapy))

Jupyter Notebook Usage
----------------------

SuryaPy works well inside Jupyter notebooks.

Install Jupyter if needed:

.. code-block:: bash

   pip install notebook

Launch Jupyter:

.. code-block:: bash

   jupyter notebook

Then import the package:

.. code-block:: python

   from suryapy import mask_sun, b_roth

Troubleshooting
---------------

Import Errors
^^^^^^^^^^^^^

If Python cannot find the package:

.. code-block:: bash

   pip uninstall suryapy==0.1.0
   pip install suryapy==0.1.0

Editable Install Not Updating
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Restart the Python kernel or reinstall:

.. code-block:: bash

   pip install -e .

PyPI Release
------------

SuryaPy is currently under active development. Features and APIs may change between releases.
