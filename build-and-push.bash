#!/bin/bash
# Builds and pushes a given image to gcr.io + all nodes in current kubectl context
set -e

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
