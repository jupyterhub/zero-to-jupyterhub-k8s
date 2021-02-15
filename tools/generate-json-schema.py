#!/usr/bin/env python3
"""
This script reads schema.yaml and generates a values.schema.json that we can
package with the Helm chart, allowing helm the CLI perform validation.

While we can directly generate a values.schema.json from schema.yaml, it
contains a lot of description text we use to generate our configuration
reference that isn't helpful to ship along the validation schema. Due to that,
we trim away everything that isn't needed.
"""

import json
import os
import sys
import yaml

from collections.abc import MutableMapping

# Change current directory to this directory
os.chdir(os.path.dirname(sys.argv[0]))


def clean_jsonschema(d, parent_key=""):
    """
    Modifies a dictionary representing a jsonschema in place to not contain
    jsonschema keys not relevant for a values.schema.json file solely for use by
    the helm CLI.
    """
    JSONSCHEMA_KEYS_TO_REMOVE = {"description"}

    # start by cleaning up the current level
    for k in set.intersection(JSONSCHEMA_KEYS_TO_REMOVE, set(d.keys())):
        print(f"Removing key: {k}, from parent_key: {parent_key}")
        del d[k]

    # Recursively cleanup nested levels, bypassing one level where there could
    # be a valid Helm chart configuration named just like the jsonschema
    # specific key to remove.
    if "properties" in d:
        for k, v in d["properties"].items():
            if isinstance(v, MutableMapping):
                clean_jsonschema(v, k)


def run():
    # Using these sets, we can validate further manually by printing the results
    # of set operations.
    with open("../jupyterhub/schema.yaml") as f:
        schema = yaml.safe_load(f)

    # Drop what isn't relevant for a values.schema.json file packaged with the
    # Helm chart, such as the description keys only relevant for our
    # configuration reference.
    clean_jsonschema(schema)

    # dump schema to values.schema.json
    with open("../jupyterhub/values.schema.json", "w") as f:
        json.dump(schema, f)


run()
