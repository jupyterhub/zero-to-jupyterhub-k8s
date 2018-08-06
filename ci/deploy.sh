#!/bin/bash

# SCRIPT SUMMARY
# --------------
# 1. Setup git and docker to be utilized by chartpress
# 2. Run chartpress

# Set shell options
# -e : Exit immediately if a command exits with a non-zero status.
# -u : Treat unset variables as an error when substituting.
set -eu

# Decrypt 'id_rsa.enc' into 'id_rsa' and make it readable only to owner
# Its a ssh identity file for having git push rights to jupyterhub/helm-chart
openssl aes-256-cbc -K $encrypted_c6b45058ffe8_key -iv $encrypted_c6b45058ffe8_iv -in cd/id_rsa.enc -out id_rsa -d
chmod 0400 id_rsa

# -x : Print commands and their arguments as they are executed.
set -x

# About 'GIT_SSH_COMMAND'
# If this environment variable is set then git fetch and git push will use the
# specified command instead of ssh when they need to connect to a remote system.
export GIT_SSH_COMMAND="ssh -i ${PWD}/id_rsa"

# ...
docker login --username "${DOCKER_USERNAME}" --password "${DOCKER_PASSWORD}"

# chartpress will...
# 1. Update Chart.yaml and values.yaml
# 2. Build and push images using docker
# 3. Publish the Helm chart on GitHub pages (jupyterhub/helm-chart) using git
chartpress --commit-range "${TRAVIS_COMMIT_RANGE}" --push --publish-chart

# Log changes to Chart.yaml and values.yaml
git diff
