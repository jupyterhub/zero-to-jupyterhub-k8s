#!/bin/sh

# Set shell options
# -e : Exit immediately if a command exits with a non-zero status.
# -u : Treat unset variables as an error when substituting.
# -x : Print commands and their arguments as they are executed.
set -eux

# Gather connection details
IP=$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}')
TEST_NAMESPACE=jupyterhub-test
TEST_URL=http://$IP:31212

# Install chart
helm upgrade jh \
    --install \
    --namespace $TEST_NAMESPACE \
    --values minikube-config.yaml \
    ./jupyterhub/

echo "waiting for servers to become responsive"
until curl --fail --silent $TEST_URL/hub/api; do
    kubectl --namespace=$TEST_NAMESPACE describe pod
    sleep 10
done

http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/docs/rest-api.yml#/
echo "getting jupyterhub version and info"
curl --silent $TEST_URL/hub/api | grep version

echo "getting jupyterhub info"
curl --silent $TEST_URL/hub/api/info

echo "spaw user"
# TODO

echo "cull user"
# TODO
