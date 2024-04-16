# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PEAT'
copyright = '2024, Regin Potter, Anmol Saini, Tiffany Behr, Matthew Sanders, Kyle Bruns'
author = 'Regin Potter, Anmol Saini, Tiffany Behr, Matthew Sanders, Kyle Bruns'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']
autodoc_mock_imports = ["RPi", "rsa", "gpiozero", "busio", "digitalio", "board", "adafruit_rfm9x", "gps3", "utils", "adafruit_ads1x15", "RPI"]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

import os
import sys
sys.path.insert(0, os.path.abspath('../.'))

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
