#!/usr/bin/env python3
"""
Run `kind load docker-image <image:tag>` on all the docker images within
values.yaml that is available locally on the host as first verified with `docker
images --quiet <image:tag>`. If we could capture this directly from chartpress
build output it would be quicker.
"""

import sys
import argparse
import pipes
import subprocess

import yaml


def check_output(cmd, **kwargs):
    """Run a subcommand and exit if it fails"""
    try:
        return subprocess.check_output(cmd, **kwargs)
    except subprocess.CalledProcessError as e:
        print(
            "`{}` exited with status {}".format(
                " ".join(map(pipes.quote, cmd)), e.returncode
            ),
            file=sys.stderr,
        )
        sys.exit(e.returncode)


def get_element_from_path(path, dictionary):
    keys = path.split(".")
    e = dictionary
    for key in keys:
        e = e[key]
    return e


def extract_images_from_values(chartpress_file, values_file):
    """Returns a list of image:tag strings given a values.yaml file."""

    with open(chartpress_file) as f:
        chartpress = yaml.full_load(f)

    with open(values_file) as f:
        values = yaml.full_load(f)

    image_paths = []
    for chart in chartpress["charts"]:
        for k, v in chart["images"].items():
            image_paths.append(v["valuesPath"])

    images = []
    for image_path in image_paths:
        image = get_element_from_path(image_path, values)
        images.append(image["name"] + ":" + image["tag"])

    return images


def kind_load_docker_images(kind_cluster, images):
    """Calls `kind load docker-image <image:tag>` on provided images available locally."""

    for image in images:
        if not check_output(["docker", "images", "--quiet", image]):
            continue

        check_output(["kind", "load", "docker-image", "--name", kind_cluster, image])
        print("### Loaded %s" % image)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--kind-cluster",
        default="kind",
        help="Specify a kind cluster to load the docker images into.",
    )
    argparser.add_argument(
        "--values",
        default="jupyterhub/values.yaml",
        help="Specify a values.yaml file to look in.",
    )
    argparser.add_argument(
        "--chartpress",
        default="chartpress.yaml",
        help="Specify a chartpress.yaml with information about where to look for images.",
    )
    args = argparser.parse_args()

    images = extract_images_from_values(
        chartpress_file=args.chartpress, values_file=args.values
    )
    kind_load_docker_images(args.kind_cluster, images)
