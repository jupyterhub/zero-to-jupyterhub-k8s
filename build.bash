#!/bin/bash
# Builds and pushes a given image to gcr.io + all nodes in current kubectl context
set -e

DOCKER_REPO=$(jq -r '.buildSettings.dockerRepo' 'docker-settings.json')
CLUSTERS=$(jq -r '.clusters | join(" ")' 'docker-settings.json')

if [ -z "$1" ]; then
	echo "Usage: $0 [ hub | proxy | base | user {user_image_type} ]"
	exit 1
fi

# Bail if we're on a dirty git tree
if ! git diff-index --quiet HEAD; then
    echo "You have uncommited changes. Please commit them before building and"
    echo "populating. This helps ensure that all docker images are traceable"
    echo "back to a git commit."
    exit 1
fi

kubectl cluster-info | grep -q azure | true
if [ ${PIPESTATUS[1]} -eq 0 ]; then
	DOCKER_PUSH="docker push"
else
	DOCKER_PUSH="gcloud docker -- push"
fi

IMAGE="$1"
GIT_REV=$(git log -n 1 --pretty=format:%h -- ${IMAGE})
TAG="${GIT_REV}"

if [ "${IMAGE}" == "user" ]; then
    USER_IMAGE_TYPE="${2}"
    DOCKERFILE="Dockerfile.${USER_IMAGE_TYPE}"
    IMAGE_SPEC="${DOCKER_REPO}/jupyterhub-k8s-${IMAGE}-${USER_IMAGE_TYPE}:${TAG}"
else
    DOCKERFILE="Dockerfile"
    IMAGE_SPEC="${DOCKER_REPO}/jupyterhub-k8s-${IMAGE}:${TAG}"
fi

cd ${IMAGE}
if [ ! -f ${DOCKERFILE} ]; then
	echo "No such file: ${IMAGE}/${DOCKERFILE}"
	exit 1
fi
docker build -t ${IMAGE_SPEC} -f ${DOCKERFILE} .
${DOCKER_PUSH} ${IMAGE_SPEC}

echo "Pushed ${IMAGE_SPEC}"
