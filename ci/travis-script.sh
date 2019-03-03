#!/bin/bash
set -eux

python3 tools/templates/lint-and-validate.py
# render & publish chart
if [[
    "$TRAVIS_BRANCH" == "master" &&
    "$TRAVIS_PULL_REQUEST" == "false" &&
    "$RUN_PUBLISH_SCRIPT" == "1"
]]; then
    ./cd/publish-chart.sh
else
    chartpress --commit-range ${TRAVIS_COMMIT_RANGE}
fi
git diff

./ci/test.sh
