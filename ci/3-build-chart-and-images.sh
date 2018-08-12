#!/bin/bash

# SCRIPT SUMMARY
# --------------
# 1. Setup docker to be utilized by chartpress
# 2. Run chartpress

# Set shell options
# -e : Exit immediately if a command exits with a non-zero status.
# -u : Treat unset variables as an error when substituting.
# -x : Print commands and their arguments as they are executed.
set -eux

# chartpress will...
# 1. Update Chart.yaml and values.yaml
# 2. Build images using docker
# 3. Build chart
chartpress --commit-range "${TRAVIS_COMMIT_RANGE}"

# Log changes to Chart.yaml and values.yaml
git diff
