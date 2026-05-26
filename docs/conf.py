# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add source directory to path
sys.path.insert(0, os.path.abspath('..'))

project = 'SuryaPy'
copyright = '2024, Soumit Dey'
author = 'Soumit Dey'
release = '0.1.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx_rtd_theme',
]

# Theme
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#FDB813',  # Solar yellow
}

# HTML output
html_static_path = ['_static']

# Napoleon settings (docstring parsing)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_method = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_annotations = False
napoleon_attr_annotations = True

# Autodoc settings
autodoc_typehints = 'description'
autodoc_member_order = 'bysource'

# Master doc
master_doc = 'index'

# Source suffix
source_suffix = '.rst'

# Pygments style
pygments_style = 'sphinx'

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
}
