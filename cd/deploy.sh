#!/bin/bash
set -eu
openssl aes-256-cbc -K $encrypted_c6b45058ffe8_key -iv $encrypted_c6b45058ffe8_iv -in cd/id_rsa.enc -out cd/id_rsa -d
set -x
chmod 0400 cd/id_rsa
docker login -u "${DOCKER_USERNAME}" -p "${DOCKER_PASSWORD}"
export GIT_SSH_COMMAND="ssh -i ${PWD}/cd/id_rsa"
chartpress --commit-range "${TRAVIS_COMMIT_RANGE}" --push --publish-chart
git diff
