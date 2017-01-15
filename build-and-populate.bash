#!/bin/bash
# Builds and pushes a given image to gcr.io + all nodes in current kubectl context
set -e

# Bail if we're on a dirty git tree
if ! git diff-index --quiet HEAD; then
    echo "You have uncommited changes. Please commit them before building and populating"
    echo "This helps ensure that all docker images are traceable back to a git commit"
    echo "If you push anyway Yuvi will be sad :("
    exit 1
fi

GIT_REV=$(git rev-parse --verify HEAD)
TAG="${GIT_REV}"
IMAGE="$1"
IMAGE_SPEC="gcr.io/data-8/jupyterhub-k8s-${IMAGE}:${TAG}"

cd ${IMAGE}
docker build -t ${IMAGE_SPEC} .
gcloud docker -- push ${IMAGE_SPEC}

echo "Pushed ${IMAGE_SPEC}"

kubectl get node --no-headers --output=custom-columns=NAME:.metadata.name | parallel gcloud compute ssh {} -- "/usr/share/google/dockercfg_update.sh && docker pull ${IMAGE_SPEC}"

echo "Use ${IMAGE_SPEC} for ${IMAGE}"
