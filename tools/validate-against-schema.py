#!/usr/bin/env python3
import jsonschema
import os
import sys
import yaml

# Change current directory to this directory
os.chdir(os.path.dirname(sys.argv[0]))

with open("../jupyterhub/schema.yaml") as f:
    schema = yaml.safe_load(f)
with open("../jupyterhub/values.yaml") as f:
    values = yaml.safe_load(f)
with open("templates/lint-and-validate-values.yaml") as f:
    lint_and_validate_values = yaml.safe_load(f)

# Validate values.yaml against schema
print("Validating values.yaml against schema.yaml...")
jsonschema.validate(values, schema)
print("OK!")
print()

# Validate lint-and-validate-values.yaml against schema
print("Validating lint-and-validate-values.yaml against schema.yaml...")
jsonschema.validate(lint_and_validate_values, schema)
print("OK!")
