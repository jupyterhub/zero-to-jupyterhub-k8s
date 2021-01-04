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
# ref: http://www.sphinx-doc.org/en/latest/extdev/tutorial.html#the-setup-function


def setup(app):
    app.add_css_file("custom.css")


# -- Referencable variables --------------------------------------------------


def _get_latest_tag():
    """Get the latest tag on a commit in branch or return None."""
    try:
        # If the git command output is my-tag-14-g0aed65e,
        # then the return value will become my-tag.
        return (
            subprocess.check_output(["git", "describe", "--tags", "--long"])
            .decode("utf-8")
            .strip()
            .rsplit("-", maxsplit=2)[0]
        )
    except subprocess.CalledProcessError:
        return None


def _get_git_ref_from_chartpress_based_version(version):
    """
    Get a git ref from a chartpress set version of format like
    1.2.3-beta.1.n123.h1234567, 1.2.3-n123.h1234567, or 1.2.3.
    """
    tag_hash_split = re.split("[\.|-]n\d\d\d\.h", version)
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

latest_tag = _get_latest_tag()
chart_version = chart["version"]
chart_version_git_ref = _get_git_ref_from_chartpress_based_version(chart_version)
jupyterhub_version = chart["appVersion"]
# FIXME: kubeVersion contain >=, but by having > in the string we substitute we
#        run into this issue:
#        https://github.com/executablebooks/MyST-Parser/issues/282
kube_version = chart["kubeVersion"].split("-", 1)[0][2:]

# These substitution variables only work in markdown contexts, and does not work
# within links etc. Reference using {{ variable_name }}
#
# myst_substitutions ref: https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html#substitutions-with-jinja2
myst_substitutions = {
    "latest_tag": latest_tag,
    "chart_version": chart_version,
    "chart_version_git_ref": chart_version_git_ref,
    "jupyterhub_version": jupyterhub_version,
    "kube_version": kube_version,
    "requirements": f"[hub/images/requirements.txt](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/{chart_version_git_ref}/images/hub/requirements.txt)",
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
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The master toctree document.
master_doc = "index"

# The suffix(es) of source filenames.
source_suffix = [".md", ".rst"]

# Rediraffe redirects to ensure proper redirection
rediraffe_redirects = {
    "customizing/user-management.html": "jupyterhub/customizing/user-management.html",
    "customizing/user-storage.html": "jupyterhub/customizing/user-storage.html",
    "customizing/user-resources.html": "jupyterhub/customizing/user-resources.html",
    "customizing/user-environment.html": "jupyterhub/customizing/user-environment.html",
    "customizing/extending-jupyterhub.html": "jupyterhub/customizing/extending-jupyterhub.html",
    "reference/glossary.html": "resources/glossary.html",
    "reference/tools.html": "resources/tools.html",
    "reference/reference-docs.html": "resources/reference-docs.html",
    "reference/reference.html": "resources/reference.html",
    "community/additional-resources.html": "resources/community.html",
    "community/users-list.html": "resources/community.html",
    "community/tips.html": "resources/community.html",
    "setup-jupyterhub/turn-off.html": "jupyterhub/uninstall.html",
    "setup-jupyterhub/setup-jupyterhub.html": "jupyterhub/installation.html",
    "setup-jupyterhub/setup-helm.html": "kubernetes/setup-helm.html",
    "ovh/step-zero-ovh.html": "kubernetes/ovh/step-zero-ovh.html",
    "digital-ocean/step-zero-digital-ocean.html": "kubernetes/digital-ocean/step-zero-digital-ocean.html",
    "ibm/step-zero-ibm.html": "kubernetes/ibm/step-zero-ibm.html",
    "redhat/step-zero-openshift.html": "kubernetes/redhat/step-zero-openshift.html",
    "amazon/step-zero-aws-eks.html": "kubernetes/amazon/step-zero-aws-eks.html",
    "amazon/step-zero-aws.html": "kubernetes/amazon/step-zero-aws.html",
    "microsoft/step-zero-azure-autoscale.html": "kubernetes/microsoft/step-zero-azure-autoscale.html",
    "microsoft/step-zero-azure.html": "kubernetes/microsoft/step-zero-azure.html",
    "google/step-zero-gcp.html": "kubernetes/google/step-zero-gcp.html",
    "create-k8s-cluster.html": "kubernetes/setup-kubernetes.html",
    "turn-off.html": "jupyterhub/uninstall.html",
    "setup-jupyterhub.html": "jupyterhub/index.html",
    "setup-helm.html": "kubernetes/setup-helm.html",
    "index-setup-jupyterhub.html": "jupyterhub/index.html",
    "tools.html": "reference/tools.html",
    "reference-docs.html": "reference/reference-docs.html",
    "index-reference.html": "resources/reference.html",
    "glossary.html": "reference/glossary.html",
    "user-storage.html": "customizing/user-storage.html",
    "user-resources.html": "customizing/user-resources.html",
    "user-management.html": "customizing/user-management.html",
    "user-environment.html": "customizing/user-environment.html",
    "index-customization-guide.html": "jupyterhub/customization.html",
    "extending-jupyterhub.html": "customizing/extending-jupyterhub.html",
    "users-list.html": "community/users-list.html",
    "tips.html": "community/tips.html",
    "index-community-resources.html": "resources/community.html#links-to-community-project-resources",
    "additional-resources.html": "resources/community.html",
    "upgrading.html": "administrator/upgrading.html",
    "troubleshooting.html": "administrator/troubleshooting.html",
    "security.html": "administrator/security.html",
    "optimization.html": "administrator/optimization.html",
    "index-administrator-guide.html": "administrator/index.html",
    "debug.html": "administrator/debug.html",
    "cost.html": "administrator/cost.html",
    "authentication.html": "administrator/authentication.html",
    "architecture.html": "administrator/architecture.html",
    "advanced.html": "administrator/advanced.html",
}


# -- Generate the Helm chart configuration reference from a schema file ------

# header
with open("resources/reference.txt", "r") as f:
    header_md = f.readlines()
header_md = header_md[1:]
header_md = [ln.strip("\n") for ln in header_md]

# schema
with open("../../jupyterhub/schema.yaml", "r") as f:
    data = yaml.safe_load(f)


def parse_schema(d, md=[], depth=0, pre=""):
    """
    Generate markdown headers from a passed python dictionary created by
    parsing a schema.yaml file.
    """
    if "properties" in d:
        depth += 1
        # Create markdown headers for each schema level
        for key, val in d["properties"].items():
            md.append("(schema_%s)=" % (pre + key))
            md.append("#" * (depth + 1) + " " + pre + key)
            md.append("")
            if "description" in val:
                for ln in val["description"].split("\n"):
                    md.append(ln)
                md.append("")

            parse_schema(val, md, depth, pre + "{}.".format(key))
        depth -= 1
    return md


schema_md = parse_schema(data)

# reference = header + schema
reference_md = header_md + schema_md
with open("resources/reference.md", "w") as f:
    f.write("\n".join(reference_md))


# -- Options for linkcheck builder -------------------------------------------
# ref: http://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder
linkcheck_ignore = [
    r"(.*)github\.com(.*)#",  # javascript based anchors
    r"(.*)/#%21(.*)/(.*)",  # /#!forum/jupyter - encoded anchor edge case
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
# ref: http://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

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
    "github_version": "master",
    "doc_path": "doc/source",
}

html_favicon = "_static/images/logo/favicon.ico"
html_logo = "_static/images/logo/logo.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
