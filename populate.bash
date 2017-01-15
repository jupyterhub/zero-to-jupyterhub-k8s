#!/bin/bash
IMAGE_SPEC="${1}"
# Pull this container in all of the nodes in current kubernetes context, 16 nodes at a time
kubectl get node --no-headers --output=custom-columns=NAME:.metadata.name | parallel -j16 "gcloud compute ssh {} -- '/usr/share/google/dockercfg_update.sh && docker pull ${IMAGE_SPEC}'"

echo "Pulled ${IMAGE_SPEC}"
