#!/bin/bash
set -eux

python3 tools/templates/lint-and-validate.py
# render & publish chart
if [[
    "$TRAVIS_BRANCH" == "master" &&
    "$TRAVIS_PULL_REQUEST" == "false" &&
    "$RUN_PUBLISH_SCRIPT" == "1"
]]; then
    ./ci/publish-chart.sh
else

    echo "is chartpress detection failing?"
    python3 -c 'import docker;  print(docker.from_env().images.get_registry_data("jupyterhub/k8s-hub:0.9-c9f80ce").id)'

    chartpress --commit-range ${TRAVIS_COMMIT_RANGE}
fi
git diff

./ci/test.sh
