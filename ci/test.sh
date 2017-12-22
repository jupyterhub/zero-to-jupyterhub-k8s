#!/bin/sh

set -eux

IP=$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}')
TEST_NAMESPACE=jupyterhub-test
TEST_URL=http://$IP:31212

helm install --name jupyterhub-test --namespace $TEST_NAMESPACE ./jupyterhub/ -f minikube-config.yaml

echo "waiting for servers to become responsive"
until curl --fail -s $TEST_URL/hub/api; do
    kubectl --namespace=$TEST_NAMESPACE describe pod
    sleep 10
done

echo "getting jupyterhub version"
curl -s $TEST_URL/hub/api | grep version
