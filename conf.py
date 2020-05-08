# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'reproduce'
copyright = 'Nicolas Tessore'
author = 'Nicolas Tessore'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.git*']

# If true, figures, tables and code-blocks are automatically numbered if they
# have a caption. The numref role is enabled. Obeyed so far only by HTML and
# LaTeX builders. Default is False.
numfig = False


# -- Options for HTML output -------------------------------------------------

# The “title” for HTML documentation generated with Sphinx’s own templates. This
# is appended to the <title> tag of individual pages, and used in the navigation
# bar as the “topmost” element. It defaults to '<project> v<revision>
# documentation'.
html_title = 'reproduce'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'agogo'

# A dictionary of options that influence the look and feel of the selected
# theme. These are theme-specific.
html_theme_options = {
    'bodyfont': '"Times New Roman", Times, serif',
    'headerfont': '"Times New Roman", Times, serif',
    'bgcolor': 'white',
    'headerbg': 'black',
    'footerbg': 'black',
    'linkcolor': 'blue',
    'headercolor1': 'inherit',
    'headercolor2': 'inherit',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# A list of JavaScript filename. The entry must be a filename string or a tuple
# containing the filename string and the attributes dictionary. The filename
# must be relative to the html_static_path, or a full URI with scheme like
# http://example.org/script.js. The attributes is used for attributes of
# <script> tag. It defaults to an empty list.
html_js_files = ['links.js']


# -- Options for LaTeX output ------------------------------------------------

latex_theme = 'howto'

latex_elements = {
    'fncychap': '',
    'figure_align': 'H',
}


# -- Intersphinx mapping -----------------------------------------------------

intersphinx_mapping = {
    'skypy': ('https://skypy.readthedocs.io/en/latest', None),
}


# -- inline extensions -------------------------------------------------------

SOURCE_URI = 'https://github.com/ntessore/reproduce/tree/master/%s'

from docutils import nodes, utils
from sphinx.util.nodes import split_explicit_title

def source_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    has_t, title, target = split_explicit_title(text)
    title = utils.unescape(title)
    target = utils.unescape(target)
    refnode = nodes.reference(title, title, refuri=SOURCE_URI % target)
    return [refnode], []

def setup(app):
    app.add_role('source', source_role)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
