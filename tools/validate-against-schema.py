#!/usr/bin/env python3
from collections.abc import MutableMapping
import jsonschema
import yaml

with open("schema.yaml") as f:
    schema = yaml.safe_load(f)

# Validate values.yaml against schema
print("Validating values.yaml...")
with open("values.yaml") as f:
    values = yaml.safe_load(f)
jsonschema.validate(values, schema)
print("OK!")
print()

# Validate lint-and-validate-values.yaml against schema
print("Validating lint-and-validate-values.yaml...")
with open("../tools/templates/lint-and-validate-values.yaml") as f:
    lint_and_validate_values = yaml.safe_load(f)
jsonschema.validate(lint_and_validate_values, schema)
print("OK!")


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


# Using these sets, you can validate further manually by printing the results of
# set operations.
schema_keys = flatten(reduce_schema(schema))
values_keys = flatten(values)
lint_and_validate_values_keys = flatten(lint_and_validate_values)

# print(values_keys - schema_keys)
