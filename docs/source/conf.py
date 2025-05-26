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
import datetime
import os
import re
import sys

import toml

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
try:
    info = toml.load("../../pyproject.toml")
except FileNotFoundError:
    info = toml.load("pyproject.toml")
project = info["project"]["name"]
copyright = str(datetime.datetime.now().year) + ", Alexander Puck Neuwirth"
author = "Alexander Puck Neuwirth"
version = re.sub("^", "", os.popen("git describe --tags").read().strip())
rst_epilog = f""".. |project| replace:: {project}"""

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "nbsphinx",
    "sphinx.ext.githubpages",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.doctest",
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.napoleon",
    "sphinx_math_dollar",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "jupyter_sphinx",
    "IPython.sphinxext.ipython_console_highlighting",
    #'sphinx_copybutton',
    #'sphinx.ext.doctest',
    #'sphinx.ext.autodoc',
    #'sphinx.ext.githubpages',
    #'nbsphinx',
    #'jupyter_sphinx',
    #'sphinx.ext.doctest',
    #'sphinx.ext.viewcode',
    #'sphinx.ext.autosummary',
    "autoapi.extension",
]
napoleon_use_ivar = True
autoapi_type = "python"
autoapi_dirs = ["../../" + project]
autoapi_python_class_content = "both"
autodoc_typehints = "description"
# autosummary_generate = True  # Turn on sphinx.ext.autosummary
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
highlight_language = "none"

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
