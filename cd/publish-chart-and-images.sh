#!/bin/bash

# SCRIPT SUMMARY
# --------------
# 1. Decrypt a ssh identity file using travis environment variables granting
#    push rights to github.com/jupyterhub/helm-chart
# 2. Setup git to utilize this ssh identity
# 3. Setup docker credentials using Travis environment variables
# 4. Run chartpress that will utilize git and docker

# Set shell options
# -e : Exit immediately if a command exits with a non-zero status.
# -u : Treat unset variables as an error when substituting.
set -eu

# Decrypt 'id_rsa.enc' into 'id_rsa' and make it readable only to owner
# Its a ssh identity file for having git push rights to jupyterhub/helm-chart
openssl aes-256-cbc -K $encrypted_c6b45058ffe8_key -iv $encrypted_c6b45058ffe8_iv -in cd/id_rsa.enc -out cd/id_rsa -d
chmod 0400 cd/id_rsa

# -x : Print commands and their arguments as they are executed.
set -x

# About 'GIT_SSH_COMMAND'
# If this environment variable is set then git fetch and git push will use the
# specified command instead of ssh when they need to connect to a remote system.
export GIT_SSH_COMMAND='ssh -i "${PWD}/cd/id_rsa"'

# ...
docker login --username "${DOCKER_USERNAME}" --password "${DOCKER_PASSWORD}"

# chartpress will...
# 0. Read instructions in ./chartpress.yaml
# 1. Build and push images using docker
# 2. Update Chart.yaml and values.yaml
# 3. Build and publish the Helm chart on GitHub pages (jupyterhub/helm-chart) using git
chartpress --commit-range "${TRAVIS_COMMIT_RANGE}" --push --publish-chart

# Log changes to Chart.yaml and values.yaml
git diff
