#!/bin/sh

# SCRIPT SUMMARY
# --------------
# 1. Install the Helm chart using minikube-config.yaml
# 2. Wait for the hub to become responsive
# 3. Ensure a user can be created, spawned and culled using the hub's API
#    http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/docs/rest-api.yml

# NOTE: The script should be executed from the repo directory

# Set shell options
# -e : Exit immediately if a command exits with a non-zero status.
# -u : Treat unset variables as an error when substituting.
# -x : Print commands and their arguments as they are executed.
set -eux

# Fetch network information
IP=$(ifconfig docker0 | grep 'inet ' | awk '{print $2}')
HUB_API_URL=http://$IP:31212/hub/api

# Install chart
helm upgrade jh \
    --install \
    --namespace jh \
    --values ci/test-config.yaml \
    ./jupyterhub/

echo "waiting for servers to become responsive"
until curl --fail --silent $HUB_API_URL; do
    kubectl describe pod --namespace jh --selector 'component in (hub,proxy,user-scheduler)'
    kubectl get pod      --namespace jh --selector 'component in (hub,proxy,user-scheduler)'
    sleep 10
done

# Make various request using the hub's API
# - 
echo "getting jupyterhub version and info"
curl --silent $TEST_URL | grep version

echo "getting jupyterhub info"
curl --silent $TEST_URL/info

echo "starting pytest"
# --verbose     : increase verbosity
# --capture=no  : no capture of output to stdout or stderr
# --exitfirst   : exit instantly on first error or failed test
pytest --verbose --capture=no --exitfirst
