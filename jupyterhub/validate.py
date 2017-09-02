#!/usr/bin/env python3
import jsonschema
import yaml

# HACK: These files are never closed, but is ok!
schema = yaml.safe_load(open('schema.yaml'))
values = yaml.safe_load(open('values.yaml'))

jsonschema.validate(values, schema)
