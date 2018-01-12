#!/bin/sh
set -e

echo "Creating Daemonset..."
# Set up
DAEMONSET=$(curl \
    -H "Content-Type: application/json"  \
    -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt  \
    -X POST \
    --fail \
    --silent \
    --show-error \
    https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}/apis/extensions/v1beta1/namespaces/${NAMESPACE}/daemonsets \
    -d "${DAEMONSET_SPEC}"
)

DAEMONSET_NAME=$(echo ${DAEMONSET} | jq -r .metadata.name)

pulling_complete() {
    NODES=$(curl \
                -H "Content-Type: application/json" \
                -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
                --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
                -X GET \
                --fail \
                --silent \
                --show-error \
                https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}/api/v1/nodes
         );

    JQ_PROGRAM='[.items[].metadata.labels[env.NODE_LABEL_KEY] == env.NODE_LABEL_VALUE] | all'
    COMPLETE=$(echo ${NODES} | jq "${JQ_PROGRAM}")
    echo ${COMPLETE}

    if [[ $COMPLETE == 'true' ]]; then
        return 0;
    else
        return 1;
    fi
}

echo "Waiting for all nodes to pull images..."
while ! pulling_complete; do
    sleep 2;
done

echo "Deleting daemonset"
curl \
    -H "Content-Type: application/json"  \
    -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt  \
    -X DELETE \
    --fail \
    --silent \
    --show-error \
    https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}/apis/extensions/v1beta1/namespaces/${NAMESPACE}/daemonsets/${DAEMONSET_NAME}

