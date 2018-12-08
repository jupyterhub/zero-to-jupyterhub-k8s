#!/bin/sh

set -eux

# Is there a standard interface name?
for iface in eth0 ens4 enp0s3; do
    IP=$(ifconfig $iface | grep 'inet addr' | cut -d: -f2 | awk '{print $1}');
    if [ -n "$IP" ]; then
        echo "IP: $IP"
        break
    fi
done
if [ -z "$IP" ]; then
    echo "Failed to get IP, current interfaces:"
    ifconfig -a
    exit 2
fi

TEST_NAMESPACE=jupyterhub-test
TEST_URL=http://$IP:31212

helm install --name jupyterhub-test --namespace $TEST_NAMESPACE ./jupyterhub/ $Z2JH_HELM_ARGS

echo "waiting for servers to become responsive"
until curl --fail -s $TEST_URL/hub/api; do
    kubectl --namespace=$TEST_NAMESPACE describe pod
    sleep 10
done

echo "getting jupyterhub version"
curl -s $TEST_URL/hub/api | grep version

# Tests seem slightly flakey on travis, automatically retry once on failure
echo "running tests"
pytest || {
  echo "tests failed, retrying once"
  pytest
}
