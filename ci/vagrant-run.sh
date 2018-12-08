#!/bin/sh
# Run this inside vagrant to test the travis scripts

set -eux
export KUBE_VERSION=1.12.3
export TRAVIS_BRANCH=master
export TRAVIS_PULL_REQUEST=true
export TRAVIS_COMMIT_RANGE=`git rev-parse --short origin/master`..`git rev-parse --short HEAD`

pip3 install --no-cache-dir -r dev-requirements.txt
. ./ci/minikube-$KUBE_VERSION.env
./ci/install.sh
./ci/travis-script.sh
