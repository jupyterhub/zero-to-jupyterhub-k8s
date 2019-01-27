#!/bin/bash
set -eux

python3 tools/templates/lint-and-validate.py
# render & publish chart
if [[
    "$TRAVIS_BRANCH" == "master" &&
    "$KUBE_VERSION" == "1.13.2" &&
    "$TRAVIS_PULL_REQUEST" == "false"
]]; then
    ./ci/deploy.sh
else
    chartpress --commit-range ${TRAVIS_COMMIT_RANGE}
fi
git diff

./ci/test.sh
