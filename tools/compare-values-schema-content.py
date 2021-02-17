#!/usr/bin/env python3
"""
This script is meant to assist in a manual validation that the content of
schema.yaml covers values.yaml, and vice versa.

FIXME: It would be nice to run this as part of our CI pipeline to report if
       schema.yaml and values.yaml gets out of sync, but first we need to
       address what it means to be out of sync.

       Consider if schema.yaml describes extraLabels, and we in this helm chart
       have an extra label set in values, how should our comparison realize that
       its nothing to bother about?

       That kind of complexity is currently an issue for labels, resources,
       containerSecurityContext, readiness- and livenessProbe's, and hub.config.
"""

import jsonschema
import os
import sys

from collections.abc import MutableMapping

import yaml

here_dir = os.path.abspath(os.path.dirname(__file__))
schema_yaml = os.path.join(here_dir, os.pardir, "jupyterhub", "schema.yaml")
values_yaml = os.path.join(here_dir, os.pardir, "jupyterhub", "values.yaml")
lint_and_validate_values_yaml = os.path.join(
    here_dir, "templates", "lint-and-validate-values.yaml"
)


def reduce_schema(d):
    """
    Takes a jsonschema loaded as a dictionary and return a reduced structure
    ignoring everything apart from the structure it describes.
    """
    r = {}
    CONTAINS_KEYS = "properties"
    if CONTAINS_KEYS in d:
        for k, v in d[CONTAINS_KEYS].items():
            if isinstance(v, MutableMapping) and v.get(CONTAINS_KEYS):
                r[k] = reduce_schema(v)
            else:
                r[k] = None
    return r


def flatten(d, parent_key="", sep="."):
    """
    Takes a nested dictionary and return all keys flattened using a separator,
    so one element returned would for example be "hub.image.tag".
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            if v:
                items.extend(flatten(v, parent_key=new_key, sep=sep))
            else:
                items.append(new_key)
        else:
            items.append(new_key)
    if not parent_key:
        return set(items)
    else:
        return items


def run():
    # Using these sets, we can validate further manually by printing the results
    # of set operations.
    with open(schema_yaml) as f:
        schema = yaml.safe_load(f)
    with open(values_yaml) as f:
        values = yaml.safe_load(f)
    # with open(lint_and_validate_values_yaml) as f:
    #     lint_and_validate_values = yaml.safe_load(f)
    schema = flatten(reduce_schema(schema))
    values = flatten(values)
    # lint_and_validate_values = flatten(lint_and_validate_values)

    print(
        "The keys from values.yaml minus those from schema.yaml:\n",
        "\n".join(sorted(values - schema)),
        "\n\n",
        sep="\n",
    )
    print(
        "The keys from schema.yaml minus those from values.yaml:\n",
        "\n".join(sorted(schema - values)),
        "\n\n",
        sep="\n",
    )


run()
