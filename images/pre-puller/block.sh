#!/bin/sh
# Script that does the following actions:
#  1. Create an image-puller daemonset to fetch the user image on all nodes
#  2. Check if all nodes have the user image present in them in a loop
#  3. When the images are present, kill the image-puller daemonset and exit
#
# All inputs are passed in as environment variables
#  1. DAEMONSET_SPEC
#     A single line JSON of the image-puller daemonset to create
#  2. KUBERNETES_SERVICE_HOST, KUBERNETES_SERVICE_PORT
#     The hostname and port to use for talking to the k8s API.
#     When running in cluster, this is automatically set by Kubernetes
#  3. IMAGE
#     Full name of user image
#  4. CURL_EXTRA_OPTIONS
#     Extra commandline options to pass to curl
#
# jq & curl are required to run this script. Complex jq scripts are kept as separate files.
#
# This script is designed to be run from inside a kubernetes cluster only.
# It will fail if any of the operations fail.
set -e

CURL_OPTIONS="--fail --silent --show-error ${CURL_EXTRA_OPTIONS}"
# Create a daemonset and capture the output from the k8s API
# When successfully created, the API output is a JSON object representing the complete spec
echo "Creating Daemonset..."
DAEMONSET=$(curl \
    -H "Content-Type: application/json"  \
    -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt  \
    -X POST \
    ${CURL_OPTIONS} \
    https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}/apis/extensions/v1beta1/namespaces/${NAMESPACE}/daemonsets \
    -d "${DAEMONSET_SPEC}"
)

# Find the generated name of the daemonset from the API response
DAEMONSET_NAME=$(echo ${DAEMONSET} | jq -r .metadata.name)

pulling_complete() {
    # Return 0 if all nodes have ${IMAGE} present in them, 1 otherwise

    # Grab definitions of all nodes in the cluster
    NODES=$(curl \
                -H "Content-Type: application/json" \
                -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
                --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
                -X GET \
                ${CURL_OPTIONS} \
                https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}/api/v1/nodes
         );

    # Find out how many nodes we have in total
    TOTAL_NODES=$(echo ${NODES} | jq -r '.items | length')

    # Find out how many nodes report having the image we care about
    COMPLETE_NODES=$(echo ${NODES} | jq -f nodes_with_image.jq --arg image ${IMAGE}| jq -r length)

    echo "${COMPLETE_NODES} of ${TOTAL_NODES} complete"
    if [[ ${COMPLETE_NODES} -eq ${TOTAL_NODES} ]]; then
        return 0;
    else
        return 1;
    fi
}

# Loop until all nodes have the image we want
echo "Waiting for all nodes to pull images..."
while ! pulling_complete; do
    sleep 2;
done

# Delete the daemonset after pulling is complete
# We set propagationPolicy to "Foreground" to have the call wait until all the pods from daemonset disappear
echo "Deleting daemonset"
curl \
    -H "Content-Type: application/json"  \
    -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt  \
    ${CURL_OPTIONS} \
    -X DELETE \
    https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}/apis/extensions/v1beta1/namespaces/${NAMESPACE}/daemonsets/${DAEMONSET_NAME} \
    -d '{"apiVersion": "v1", "kind": "DeleteOptions", "propagationPolicy": "Foreground"}'

