#!/usr/bin/env python3
from functools import lru_cache
import os
from subprocess import check_call

import click
from ruamel.yaml import YAML

yaml = YAML()
here = os.path.dirname(os.path.abspath(__file__))
chartpress_yaml = os.path.join(here, os.pardir, os.pardir, "chartpress.yaml")
values_yaml = os.path.join(here, os.pardir, os.pardir, "jupyterhub", "values.yaml")
image = 'hub-dependencies'


@lru_cache()
def build_args(image='hub'):
    """retrieve docker build arguments from"""
    with open(chartpress_yaml) as f:
        chartpress_config = yaml.load(f)
    chart = chartpress_config['charts'][0]
    image = chart['images'][image]
    return image.get('buildArgs', {})


def build_image():
    click.echo(f"Building image {image}")
    build_arg_dict = build_args()
    build_arg_list = []
    for key in sorted(build_arg_dict):
        value = build_arg_dict[key]
        build_arg_list.append("--build-arg")
        build_arg_list.append(f"{key}={value}")
    check_call(["docker", "build", "-t", image] + build_arg_list + [here])


@click.group()
def cli():
    pass


@click.command()
@click.argument('packages', nargs=-1)
def freeze(packages):
    """freeze the environment, optionally upgrading packages"""
    build_image()
    click.echo("freezing dependencies with pip-compile")
    upgrade_args = []
    for package in packages:
        upgrade_args.append("--upgrade-package")
        upgrade_args.append(package)
    check_call(
        [
            "docker",
            "run",
            "--rm",
            "-it",
            "--volume",
            f"{here}:/io",
            "--workdir",
            "/io",
            image,
            "pip-compile",
        ] + upgrade_args
    )


cli.add_command(freeze)


@click.command()
def outdated():
    """Check for outdated dependencies with pip"""
    build_image()
    click.echo("Checking for outdated dependencies with pip")
    check_call(["docker", "run", "--rm", "-it", image, "pip", "list", "--outdated"])


cli.add_command(outdated)


if __name__ == '__main__':
    cli()
