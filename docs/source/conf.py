# Configuration file for Sphinx to build our documentation to HTML.
#
# Configuration reference: https://www.sphinx-doc.org/en/master/usage/configuration.html
#

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project specific imports ------------------------------------------------

import datetime
import os
import re
import subprocess

import yaml

# -- Sphinx setup function ---------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx-core-events


def setup(app):
    app.add_css_file("custom.css")


# -- Referenceable variables --------------------------------------------------


def _get_git_ref_from_chartpress_based_version(version):
    """
    Get a git ref from a chartpress set version of format like
    1.2.3-beta.1.n123.h1234567, 1.2.3-n123.h1234567, or 1.2.3.
    """
    tag_hash_split = re.split(r"[\.|-]n\d\d\d\.h", version)
    if len(tag_hash_split) == 2:
        return tag_hash_split[1]
    else:
        return tag_hash_split[0]


# FIXME: Stop relying on chartpress to modify Chart.yaml (and values.yaml) by
#        creating a new feature of chartpress that allows us to directly acquire
#        the dynamically set chart version from Chart.yaml. This would be
#        similar to the --list-images feature of chartpress.
subprocess.run(["chartpress", "--skip-build"], cwd=os.path.abspath("../.."))
with open("../../jupyterhub/Chart.yaml") as f:
    chart = yaml.safe_load(f)
subprocess.run(["chartpress", "--reset"], cwd=os.path.abspath("../.."))

# These substitution variables only work in markdown contexts, and does not work
# within links etc. Reference using {{ variable_name }}
#
# myst_substitutions ref: https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html#substitutions-with-jinja2
myst_substitutions = {
    "chart_version": chart["version"],
    "jupyterhub_version": chart["appVersion"],
    # FIXME: kubeVersion contain >=, but by having > in the string we substitute
    #        we run into this issue:
    #        https://github.com/executablebooks/MyST-Parser/issues/282
    "kube_version": chart["kubeVersion"].split("-", 1)[0][2:],
    "helm_version": "3.5",
    "requirements": f"[hub/images/requirements.txt](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/{_get_git_ref_from_chartpress_based_version(chart['version'])}/images/hub/requirements.txt)",
}


# -- General MyST configuration -----------------------------------------------------

# myst_enable_extensions ref: https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html
myst_enable_extensions = [
    "substitution",
]


# -- Project information -----------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Zero to JupyterHub with Kubernetes"
copyright = f"{datetime.date.today().year}, Project Jupyter Contributors"
author = "Project Jupyter Contributors"


# -- General Sphinx configuration ---------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Set the default role so we can use `foo` instead of ``foo``
default_role = "literal"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
    "myst_parser",
    "sphinxext.rediraffe",
    "sphinxext.opengraph",
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The root toctree document.
root_doc = master_doc = "index"

# The suffix(es) of source filenames.
source_suffix = [".md", ".rst"]

# Rediraffe redirects to ensure proper redirection
rediraffe_redirects = {
    "customizing/user-management": "jupyterhub/customizing/user-management",
    "customizing/user-storage": "jupyterhub/customizing/user-storage",
    "customizing/user-resources": "jupyterhub/customizing/user-resources",
    "customizing/user-environment": "jupyterhub/customizing/user-environment",
    "customizing/extending-jupyterhub": "jupyterhub/customizing/extending-jupyterhub",
    "reference/glossary": "resources/glossary",
    "reference/tools": "resources/tools",
    "reference/reference-docs": "resources/reference-docs",
    "reference/reference": "resources/reference",
    "community/additional-resources": "resources/community",
    "community/users-list": "resources/community",
    "community/tips": "resources/community",
    "setup-jupyterhub/turn-off": "jupyterhub/uninstall",
    "setup-jupyterhub/setup-jupyterhub": "jupyterhub/installation",
    "setup-jupyterhub/setup-helm": "kubernetes/setup-helm",
    "ovh/step-zero-ovh": "kubernetes/ovh/step-zero-ovh",
    "digital-ocean/step-zero-digital-ocean": "kubernetes/digital-ocean/step-zero-digital-ocean",
    "ibm/step-zero-ibm": "kubernetes/ibm/step-zero-ibm",
    "redhat/step-zero-openshift": "kubernetes/redhat/step-zero-openshift",
    "amazon/step-zero-aws-eks": "kubernetes/amazon/step-zero-aws-eks",
    "amazon/step-zero-aws": "kubernetes/amazon/step-zero-aws",
    "microsoft/step-zero-azure-autoscale": "kubernetes/microsoft/step-zero-azure",
    "microsoft/step-zero-azure": "kubernetes/microsoft/step-zero-azure",
    "google/step-zero-gcp": "kubernetes/google/step-zero-gcp",
    "create-k8s-cluster": "kubernetes/setup-kubernetes",
    "turn-off": "jupyterhub/uninstall",
    "setup-jupyterhub": "jupyterhub/index",
    "setup-helm": "kubernetes/setup-helm",
    "index-setup-jupyterhub": "jupyterhub/index",
    "tools": "reference/tools",
    "reference-docs": "reference/reference-docs",
    "index-reference": "resources/reference",
    "glossary": "reference/glossary",
    "user-storage": "customizing/user-storage",
    "user-resources": "customizing/user-resources",
    "user-management": "customizing/user-management",
    "user-environment": "customizing/user-environment",
    "index-customization-guide": "jupyterhub/customization",
    "extending-jupyterhub": "customizing/extending-jupyterhub",
    "users-list": "community/users-list",
    "tips": "community/tips",
    "index-community-resources": "resources/community",
    "additional-resources": "resources/community",
    "upgrading": "administrator/upgrading/index",
    "troubleshooting": "administrator/troubleshooting",
    "security": "administrator/security",
    "optimization": "administrator/optimization",
    "index-administrator-guide": "administrator/index",
    "debug": "administrator/debug",
    "cost": "administrator/cost",
    "authentication": "administrator/authentication",
    "architecture": "administrator/architecture",
    "advanced": "administrator/advanced",
}

# opengraph configuration
# ogp_site_url/prefix is set automatically by RTD
ogp_image = "_static/logo.png"
ogp_use_first_image = True

# -- Generate the Helm chart configuration reference from a schema file ------

# header
with open("resources/reference.txt") as f:
    header_md = f.readlines()
header_md = header_md[1:]
header_md = [ln.strip("\n") for ln in header_md]

# schema
with open("../../jupyterhub/schema.yaml") as f:
    data = yaml.safe_load(f)


def parse_schema(d, md=[], depth=0, pre=""):
    """
    Generate markdown headers from a passed python dictionary created by
    parsing a schema.yaml file.
    """
    if "then" in d:
        d = d["then"]

    if "properties" in d:
        depth += 1
        # Create markdown headers for each schema level
        for key, val in d["properties"].items():
            md.append(f"(schema_{pre}{key})=")
            md.append("#" * (depth + 1) + f" {pre}{key}")
            md.append("")
            if "description" in val:
                for ln in val["description"].split("\n"):
                    md.append(ln)
                md.append("")

            parse_schema(val, md, depth, f"{pre}{key}.")
        depth -= 1
    return md


schema_md = parse_schema(data)

# reference = header + schema
reference_md = header_md + schema_md
with open("resources/reference.md", "w") as f:
    f.write("\n".join(reference_md))


# -- Options for linkcheck builder -------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder
linkcheck_ignore = [
    r"(.*)github\.com(.*)#",  # javascript based anchors
    r"(.*)/#%21(.*)/(.*)",  # /#!forum/jupyter - encoded anchor edge case
    r"https://github.com/[^/]*$",  # too many github usernames / searches in changelog
    "https://github.com/jupyterhub/zero-to-jupyterhub-k8s/pull/",  # too many PRs in changelog
    "https://github.com/jupyterhub/zero-to-jupyterhub-k8s/compare/",  # too many comparisons in changelog
    "https://your-domain.com",  # example
    "https://your-domain-name.com",  # example
    "https://kubernetes.io/docs/tutorials/kubernetes-basics/",  # works
    "https://cloud.ibm.com/kubernetes/catalog/create",  # works
    "https://portal.azure.com",  # sign-in redirect noise
    "https://console.cloud.google.com",  # sign-in redirect noise
    "https://console.developers.google.com",  # sign-in redirect noise
]
linkcheck_anchors_ignore = [
    "/#!",
    "/#%21",
]


# -- Options for HTML output -------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/jupyterhub/zero-to-jupyterhub-k8s/",
    "use_edit_page_button": True,
}
html_context = {
    "github_user": "jupyterhub",
    "github_repo": "zero-to-jupyterhub-k8s",
    "github_version": "main",
    "doc_path": "docs/source",
}

html_favicon = "_static/images/logo/favicon.ico"
html_logo = "_static/images/logo/logo.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
