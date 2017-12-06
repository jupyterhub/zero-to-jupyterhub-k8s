#!/bin/sh

set -eux

IP=$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}')
TEST_NAMESPACE=jupyterhub-test
TEST_URL=http://$IP:31212

helm install --name jupyterhub-test --namespace $TEST_NAMESPACE ./jupyterhub/ -f minikube-config.yaml

echo "waiting for pods to become ready"
JSONPATH='{range .items[*]}{@.status.phase};{end}'
until kubectl get pod --namespace $TEST_NAMESPACE -o jsonpath="$JSONPATH" | grep -q -i "^\(running;\)\+$"; do
    kubectl get pod --namespace $TEST_NAMESPACE
    sleep 5
done

echo "waiting for servers to become responsive"
until curl -s $TEST_URL > /dev/null; do
    sleep 5
done

echo "getting jupyterhub version"
curl -s $TEST_URL/hub/api | grep version
