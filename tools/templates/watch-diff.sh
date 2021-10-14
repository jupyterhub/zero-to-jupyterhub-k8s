#!/bin/bash
# Use https://www.shellcheck.net/ to reduce mistakes if you make changes to this file.
#
# This script is a quick and dirty solution to monitoring how work done to
# templates influence the rendered resource manifests. When you start this
# script, the templates as they currently render become a comparison point which
# "git diff" is then updated against.
#

# https://stackoverflow.com/a/246128
HERE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TMP_DIFF_DIR=/tmp/diff

# initialize by committing the current state to a dummy directory
set -eu
rm -rf $TMP_DIFF_DIR
mkdir $TMP_DIFF_DIR
git init $TMP_DIFF_DIR

helm template jupyterhub --values "$HERE_DIR/lint-and-validate-values.yaml" --output-dir $TMP_DIFF_DIR

# create a point of comparison
(cd $TMP_DIFF_DIR && git add . && git commit -m "Comparision point")

# watch "git diff" every second (-n1), in color (-c), without watch header (-t)
watch -n1 -ct "helm template jupyterhub --values \"$HERE_DIR/lint-and-validate-values.yaml\" --output-dir $TMP_DIFF_DIR > /dev/null && (cd $TMP_DIFF_DIR && git diff --unified=1 --color=always)"
