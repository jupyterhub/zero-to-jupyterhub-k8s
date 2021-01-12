#!/bin/bash
#
# In .github/workflows/test-chart.yaml, we test upgrading one chart version to
# another. After having installed the first version we run "helm diff" with the
# new version.
#
# This script created to be referenced by helm's --post-renderer flag to replace
# strings in the rendered templates into something that doesn't change.
#

set -eu
sed -e "s|$STRING_REPLACER_A|$STRING_REPLACER_B|" < /dev/stdin
