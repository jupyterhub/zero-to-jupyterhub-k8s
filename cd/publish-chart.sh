#!/bin/bash
set -eu

# Decrypt a private SSH key having its public key registered on GitHub. It will
# be used to establish an identity with rights to push to the repo hosting our
# Helm charts: https://github.com/jupyterhub/helm-chart
openssl aes-256-cbc -K $encrypted_c6b45058ffe8_key -iv $encrypted_c6b45058ffe8_iv -in cd/id_rsa.enc -out cd/id_rsa -d
chmod 0400 cd/id_rsa

docker login -u "${DOCKER_USERNAME}" -p "${DOCKER_PASSWORD}"

# Activate logging of bash commands now that the sensitive stuff is done
set -x

# As chartpress utilizes git to push to our Helm chart repository, we configure
# git ahead of time to utilize the identity we decrypted earlier.
export GIT_SSH_COMMAND="ssh -i ${PWD}/cd/id_rsa"

chartpress --commit-range "${TRAVIS_COMMIT_RANGE}" --push --publish-chart

# Let us log the changes chartpress did, it should include replacements for
# fields in values.yaml, such as what tag for various images we are using.
git diff
