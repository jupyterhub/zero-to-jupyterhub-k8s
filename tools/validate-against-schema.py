#!/usr/bin/env python3
import jsonschema
import yaml

with open("schema.yaml") as f:
    schema = yaml.safe_load(f)

# Validate values.yaml against schema
print("Validating values.yaml against schema.yaml...")
with open("values.yaml") as f:
    values = yaml.safe_load(f)
jsonschema.validate(values, schema)
print("OK!")
print()

# Validate lint-and-validate-values.yaml against schema
print("Validating lint-and-validate-values.yaml against schema.yaml...")
with open("../tools/templates/lint-and-validate-values.yaml") as f:
    lint_and_validate_values = yaml.safe_load(f)
jsonschema.validate(lint_and_validate_values, schema)
print("OK!")
