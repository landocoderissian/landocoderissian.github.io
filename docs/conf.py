# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'CharMorph'
author = 'Hopefullyidontgetbanned'
copyright = '2024, Upliner'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'style_nav_header_background': 'green',  # Set the header background to green
    'collapse_navigation': False,  # Show full file tree in the sidebar
    'sticky_navigation': True,  # Keep the navigation sticky
    'navigation_depth': 4,  # Adjust the depth of the navigation tree
    'titles_only': False,  # Show both titles and toctrees in sidebar
}

html_static_path = ['_static']

# Custom CSS and JavaScript
def setup(app):
    app.add_css_file('custom.css')
    app.add_js_file('custom.js')  # Include the custom JavaScript file
