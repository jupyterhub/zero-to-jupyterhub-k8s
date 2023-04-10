#!/usr/bin/env python3
"""
This script is meant to help compare the entries in values.schema.yaml with the
entries in values.yaml and lint-and-validate-values.yaml.

Running this script can result in output like:

    values.schema.yaml entries not found in values.yaml:
    - hub.deploymentStrategy.rollingUpdate
    - hub.fsGid
    - rbac.enabled
"""

import os
from collections.abc import MutableMapping

import yaml

here_dir = os.path.abspath(os.path.dirname(__file__))
schema_yaml = os.path.join(here_dir, os.pardir, "jupyterhub", "values.schema.yaml")
values_yaml = os.path.join(here_dir, os.pardir, "jupyterhub", "values.yaml")
lint_values_yaml = os.path.join(here_dir, "templates", "lint-and-validate-values.yaml")


def reduce_schema(d):
    """
    Takes a jsonschema loaded as a dictionary and return a reduced structure
    ignoring everything apart from the structure it describes.

    If additionalProperties or patternProperties is set, a "*" key will be added
    instead of whats listed under "properties".
    """
    r = {}
    if "properties" in d:
        for k, v in d["properties"].items():
            r[k] = None
            if isinstance(v, MutableMapping):
                if v.get("additionalProperties") or v.get("patternProperties"):
                    r[k] = {"*": None}
                # Exception: The schema describes conditional properties based
                #            on a condition in an "if" key. Then assume we want
                #            the properties found in the "then" key.
                #
                elif v.get("then", {}).get("properties"):
                    r[k] = reduce_schema(v["then"])
                elif v.get("properties"):
                    r[k] = reduce_schema(v)
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
                items.append(new_key)
                items.extend(flatten(v, parent_key=new_key, sep=sep))
            else:
                items.append(new_key)
        else:
            items.append(new_key)
    if not parent_key:
        items = set(items)
    return items


def startswith_any_element_in_list(string, in_list):
    for s in in_list:
        if string.startswith(s):
            return True
    return False


def get_schema_values_diff(values_file, schema, schema_wildcards):
    with open(values_file) as f:
        values = yaml.safe_load(f)
    values = flatten(values)
    return {
        v
        for v in schema - values
        if not startswith_any_element_in_list(v, schema_wildcards)
    }


def run():
    with open(schema_yaml) as f:
        schema = yaml.safe_load(f)
    schema = flatten(reduce_schema(schema))
    schema_wildcards = {l[:-2] for l in schema if l.endswith(".*")}
    schema = {l for l in schema if not l.endswith(".*")}

    schema_values_diff = get_schema_values_diff(values_yaml, schema, schema_wildcards)
    if schema_values_diff:
        print("values.schema.yaml entries not found in values.yaml:")
        for l in sorted(schema_values_diff):
            print(f"- {l}")

    lint_schema_values_diff = get_schema_values_diff(
        lint_values_yaml, schema, schema_wildcards
    )
    if lint_schema_values_diff:
        print("values.schema.yaml entries not found in lint-and-validate-values.yaml:"),
        for l in sorted(lint_schema_values_diff):
            print(f"- {l}")


run()
