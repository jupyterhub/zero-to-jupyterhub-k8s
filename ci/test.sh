#!/bin/sh

set -eux

IP=$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}')
TEST_NAMESPACE=jupyterhub-test
TEST_URL=http://$IP:31212

helm install --name jupyterhub-test --namespace $TEST_NAMESPACE ./jupyterhub/ -f minikube-config.yaml

kubectl --namespace=$TEST_NAMESPACE rollout status --watch deployment/hub
kubectl --namespace=$TEST_NAMESPACE rollout status --watch deployment/proxy

echo "waiting for servers to become responsive"
until curl -s $TEST_URL/hub/api; do
    sleep 5
done

echo "getting jupyterhub version"
curl -s $TEST_URL/hub/api | grep version
