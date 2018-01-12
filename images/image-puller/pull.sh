#!/bin/sh
set -e
AUTH=""

case $IMAGE in gcr.io*)
                   # gcr.io is being used, assume we are on GKE & authenticate with the metadata service for pulling
                   PWD=$(curl -s -f -m 10 "http://metadata/computeMetadata/v1/instance/service-accounts/default/token" -H "Metadata-Flavor: Google" \
                             | jq -r .access_token)

                   AUTH=$(echo -n "{\"username\": \"_token\", \"email\": \"notval@goo.com\", \"password\": \"${PWD}\"}" \
                              | base64 \
                              | tr -d '\n')
esac

curl -H "X-Registry-Auth: ${AUTH}" -X POST --unix-socket /var/run/docker.sock "http:/v1.23/images/create?fromImage=${IMAGE}&tag=${TAG}"

curl  \
    -H "Content-Type: application/merge-patch+json"  \
    -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt  \
    -X PATCH \
    https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}/api/v1/nodes/${NODE} \
    -d "{\"metadata\": {\"labels\": {\"${NODE_LABEL_KEY}\":\"${NODE_LABEL_VALUE}\"}}}"
