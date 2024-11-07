# Configuration file for Sphinx to build our documentation to HTML.
#
# Configuration reference: https://www.sphinx-doc.org/en/master/usage/configuration.html
#
import datetime
import json
import os
import re
import subprocess

import yaml

# -- Project information -----------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
#
project = "Zero to JupyterHub with Kubernetes"
copyright = f"{datetime.date.today().year}, Project Jupyter Contributors"
author = "Project Jupyter Contributors"


# -- General Sphinx configuration ---------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
#
extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinxext.opengraph",
    "sphinxext.rediraffe",
]
root_doc = "index"
source_suffix = [".md"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- General MyST configuration -----------------------------------------------------
# ref: https://myst-parser.readthedocs.io/en/latest/configuration.html
#
myst_enable_extensions = [
    "colon_fence",
    "substitution",
]


# -- Referenceable variables --------------------------------------------------
#
def _get_git_ref_from_chartpress_based_version(version):
    """
    Get a git ref from a chartpress set version of format like
    - 2.0.1-0.dev.git.5810.hf475e7a4 return git hash
    - 2.0.0-beta.1 return tag
    - 2.0.0 return tag
    """
    m = re.match(r"\d+\.\d+\.\d+(-.+\.h([0-9a-f]+))$", version)
    if m:
        return m.group(2)
    return version


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


# -- Generate the Helm chart configuration reference from a schema file ------
#
# header
with open("resources/reference.txt") as f:
    header_md = f.readlines()
header_md = header_md[1:]
header_md = [ln.strip("\n") for ln in header_md]

# schema
with open("../../jupyterhub/values.schema.yaml") as f:
    data = yaml.safe_load(f)


# default_values
with open("../../jupyterhub/values.yaml") as f:
    default_values = yaml.safe_load(f)


def get_default_value(k):
    """
    Get the default value from values.yaml
    """
    v = default_values
    for key in k.split("."):
        v = v[key]
    return v


def parse_schema(d, md=[], depth=0, pre=""):
    """
    Generate markdown headers from a passed python dictionary created by
    parsing a values.schema.yaml file.
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
            try:
                def_value = get_default_value(f"{pre}{key}")
                if (
                    def_value is not None
                    and not isinstance(def_value, dict)
                    and def_value
                    not in (
                        "set-by-chartpress",
                        "",
                    )
                ):
                    # Use the JSON string representation instead of Python
                    md.append(f"_Default:_ `{json.dumps(def_value)}`")
                    md.append("")
            except KeyError:
                # TODO: Should we error if the property isn't in values.yaml?
                pass

            parse_schema(val, md, depth, f"{pre}{key}.")
        depth -= 1
    return md


schema_md = parse_schema(data)

# reference = header + schema
reference_md = header_md + schema_md
with open("resources/reference.md", "w") as f:
    f.write("\n".join(reference_md))


# -- Options for intersphinx extension ---------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration
#
# The extension makes us able to link like to other projects like below.
#
#     rST  - :external:py:class:`tornado.httpclient.AsyncHTTPClient`
#     MyST - {external:py:class}`tornado.httpclient.AsyncHTTPClient`
#
# To see what we can link to, do the following where "objects.inv" is appended
# to the sphinx based website:
#
#     python -m sphinx.ext.intersphinx https://jupyterhub.readthedocs.io/en/stable/objects.inv
#
intersphinx_mapping = {
    "jupyterhub": ("https://jupyterhub.readthedocs.io/en/stable/", None),
    "oauthenticator": ("https://oauthenticator.readthedocs.io/en/stable/", None),
    "kubespawner": ("https://jupyterhub-kubespawner.readthedocs.io/en/stable/", None),
}

# intersphinx_disabled_reftypes set based on recommendation in
# https://docs.readthedocs.io/en/stable/guides/intersphinx.html#using-intersphinx
intersphinx_disabled_reftypes = ["*"]


# -- Options for HTML output -------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
#
html_logo = "_static/images/logo/logo.png"
html_favicon = "_static/images/logo/favicon.ico"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# pydata_sphinx_theme reference: https://pydata-sphinx-theme.readthedocs.io/en/latest/
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


# -- Readthedocs specific configuration -------------------------------------------
# ref: https://about.readthedocs.com/blog/2024/07/addons-by-default/
#
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")
if os.environ.get("READTHEDOCS", "") == "True":
    html_context["READTHEDOCS"] = True


# -- Options for linkcheck builder -------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder
#
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
    "https://github.com/traefik/traefik/blob/HEAD/CHANGELOG.md",  # works
    "https://portal.azure.com",  # sign-in redirect noise
    "https://console.cloud.google.com",  # sign-in redirect noise
    "https://console.developers.google.com",  # sign-in redirect noise
]
linkcheck_anchors_ignore = [
    "/#!",
    "/#%21",
]


# -- Options for the opengraph extension -------------------------------------
# ref: https://github.com/wpilibsuite/sphinxext-opengraph#options
#
# This extension help others provide better thumbnails and link descriptions
# when they link to this documentation from other websites, such as
# https://discourse.jupyter.org.
#
# ogp_site_url is set automatically by RTD
ogp_image = "_static/logo.png"
ogp_use_first_image = True


# -- Options for the rediraffe extension -------------------------------------
# ref: https://github.com/wpilibsuite/sphinxext-rediraffe#readme
#
# This extensions help us relocated content without breaking links. If a
# document is moved internally, we should configure a redirect like below.
#
rediraffe_branch = "main"
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
    "kubernetes/other-infrastructure/step-zero-microk8s": "kubernetes/other-infrastructure/step-zero-other",
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
