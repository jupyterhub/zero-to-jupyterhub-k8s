
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


# -- Project specific imports ------------------------------------------------

from datetime import date

import yaml


# -- Sphinx setup function ---------------------------------------------------
# ref: http://www.sphinx-doc.org/en/latest/extdev/tutorial.html#the-setup-function

def setup(app):
    app.add_css_file('custom.css')


# -- Project information -----------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Zero to JupyterHub with Kubernetes'
copyright = '{year}, Project Jupyter Contributors'.format(year=date.today().year)
author = 'Project Jupyter Contributors'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
with open('../../jupyterhub/Chart.yaml') as f:
    chart = yaml.safe_load(f)
version = chart['version'].split('-', 1)[0]
release = chart['version']

# Project specific variables
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-rst_epilog
rst_epilog = """
.. |hub_version| replace:: {v}
""".format(v=chart['appVersion'])


# -- General configuration ---------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Set the default role so we can use `foo` instead of ``foo``
default_role = 'literal'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.mathjax',
              'sphinx_copybutton',
              'myst_parser']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The master toctree document.
master_doc = 'index'

# The suffix(es) of source filenames.
source_suffix = ['.rst', '.md']


# -- Generate the Helm chart configuration reference from a schema file ------

# header
with open('reference/reference.txt', 'r') as f:
    header_md = f.readlines()
header_md = header_md[1:]
header_md = [ln.strip('\n') for ln in header_md]

# schema
with open('../../jupyterhub/schema.yaml', 'r') as f:
    data = yaml.safe_load(f)
def parse_schema(d, md=[], depth=0, pre=''):
    """
    Generate markdown headers from a passed python dictionary created by
    parsing a schema.yaml file.
    """
    if 'properties' in d:
        depth += 1
        # Create markdown headers for each schema level
        for key, val in d['properties'].items():
            md.append("(schema:%s)=" % (pre + key))
            md.append('#'*(depth + 1) + ' ' + pre + key)
            md.append('')
            if 'description' in val:
                for ln in val['description'].split('\n'):
                    md.append(ln)
                md.append('')

            parse_schema(val, md, depth, pre+'{}.'.format(key))
        depth -= 1
    return md
schema_md = parse_schema(data)

# reference = header + schema
reference_md = header_md + schema_md
with open('reference/reference.md', 'w') as f:
    f.write('\n'.join(reference_md))


# -- Options for linkcheck builder -------------------------------------------
# ref: http://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder
linkcheck_ignore = [
    r'(.*)github\.com(.*)#',                                    # javascript based anchors
    r'(.*)/#%21(.*)/(.*)',                                      # /#!forum/jupyter - encoded anchor edge case
    "https://your-domain.com",                                  # example
    "https://your-domain-name.com",                             # example
    "https://kubernetes.io/docs/tutorials/kubernetes-basics/",  # works
    "https://cloud.ibm.com/kubernetes/catalog/create",          # works
]
linkcheck_anchors_ignore = [
    "/#!",
    "/#%21",
]


# -- Options for HTML output -------------------------------------------------
# ref: http://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "github_url": "https://github.com/jupyterhub/zero-to-jupyterhub-k8s/",
    "use_edit_page_button": True,
}
html_context = {
    "github_user": "jupyterhub",
    "github_repo": "zero-to-jupyterhub-k8s",
    "github_version": "master",
    "doc_path":"doc",
}

html_favicon = '_static/images/logo/favicon.ico'
html_logo = '_static/images/logo/logo.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']




# -- Below are options for more esoteric output -------------------------------
# -----------------------------------------------------------------------------


# -- Options for HTML help output ---------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-help-output

# Output file base name for HTML help builder.
htmlhelp_basename = 'ZeroToJupyterhubDoc'


# -- Options for LaTeX output ------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-latex-output

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files.
latex_documents = [
    (
        master_doc,                     # source start file
        'ZeroToJupyterhubDoc.tex',      # target name
        'Zero to JupyterHub',           # title
        author,                         # author
        'manual'                        # documentclass [howto, manual, or own class]
    ),
]


# -- Options for manual page output ------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-manual-page-output

# One entry per manual page.
man_pages = [
    (
        master_doc,             # source start file
        'zerotojupyterhub',     # name
        'Zero to JupyterHub',   # description
        [author],               # authors
        1,                      # manual section
    ),
]


# -- Options for Texinfo output ----------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-texinfo-output

# Grouping the document tree into Texinfo files.
texinfo_documents = [
    (
        master_doc,                         # source start file
        'ZeroToJupyterhubDoc',              # target name
        'Zero to JupyterHub',               # title
        author,                             # author
        'ZeroToJupyterhubDoc',              # dir menu entry
        'One line description of project.', # description
        'Miscellaneous'                     # category
    ),
]


# -- Options for epub output -------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-epub-output

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']
