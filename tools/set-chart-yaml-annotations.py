#!/usr/bin/env python3
"""
This script inspects the images used by the chart and updates Chart.yaml's
annotations. Specifically, an annotation read by artificathub.io. For more
information, see this issue describing why we want this:

https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues/2044

FIXME: This implementation is done quick and dirty by appending to Chart.yaml
       instead of loading it, updating it, and writing content back.
"""

import os
import textwrap
from collections.abc import MutableMapping

import yaml

here_dir = os.path.abspath(os.path.dirname(__file__))
values_yaml = os.path.join(here_dir, os.pardir, "jupyterhub", "values.yaml")
chart_yaml = os.path.join(here_dir, os.pardir, "jupyterhub", "Chart.yaml")


def find_images(values, images=None):
    """
    Searches through values.yaml for images and their tags and returns a list of
    "<image>:<tag>" strings.
    """
    if images == None:
        images = []

    for k, v in values.items():
        if isinstance(v, MutableMapping):
            if k == "image":
                if "name" in v and "tag" in v:
                    images.append(f"{v['name']}:{v['tag']}")
            else:
                find_images(v, images)
    return sorted(images)


def run():
    with open(values_yaml) as f:
        values = yaml.safe_load(f)

    images = find_images(values)

    images_artifacthub_format = textwrap.indent(
        yaml.dump(
            [{"name": i.split(":")[0].split("/")[-1], "image": i} for i in images]
        ),
        "    ",
    )
    chart_yaml_appendix = (
        "annotations:\n" + '  "artifacthub.io/images": |\n' + images_artifacthub_format
    )

    print("Appending the following to Chart.yaml:\n")
    print(chart_yaml_appendix)

    with open(chart_yaml, "a") as f:
        f.write(chart_yaml_appendix)

    print("jupyterhub/Chart.yaml annotations updated")


run()
