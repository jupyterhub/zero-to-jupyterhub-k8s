#!/bin/sh

set -eux

# Is there a standard interface name?
for iface in eth0 ens4 enp0s3; do
    IP=$(/sbin/ifconfig $iface | grep 'inet addr' | cut -d: -f2 | awk '{print $1}');
    if [ -n "$IP" ]; then
        echo "IP: $IP"
        break
    fi
done
if [ -z "$IP" ]; then
    echo "Failed to get IP, current interfaces:"
    /sbin/ifconfig -a
    exit 2
fi

TEST_NAMESPACE=jupyterhub-test

helm install --wait --name jupyterhub-test --namespace $TEST_NAMESPACE ./jupyterhub/ $Z2JH_HELM_ARGS

if [ "$RUNNER" = "kind" ]; then
  kubectl port-forward -n $TEST_NAMESPACE svc/proxy-public 8080:80 &
  TEST_URL=http://127.0.0.1:8080
  export HUB_API_URL=http://127.0.0.1:8080/hub/api
else
  TEST_URL=http://$IP:31212
fi

echo "waiting for servers to become responsive"
until curl --fail -s $TEST_URL/hub/api; do
    kubectl --namespace=$TEST_NAMESPACE describe pod
    sleep 10
done

echo "getting jupyterhub version"
curl -s $TEST_URL/hub/api | grep version

echo "running tests"

display_logs() {
  echo "***** minikube *****"
  minikube logs
  echo "***** node *****"
  kubectl describe node
  echo "***** pods *****"
  kubectl --namespace $TEST_NAMESPACE get pods
  echo "***** events *****"
  kubectl --namespace $TEST_NAMESPACE get events
  echo "***** hub *****"
  kubectl --namespace $TEST_NAMESPACE logs deploy/hub
  echo "***** proxy *****"
  kubectl --namespace $TEST_NAMESPACE logs deploy/proxy
}

# Run this first to ensure the hub can talk to the proxy
# (it will automatically retry)
pytest tests/test_hub_is_ready.py

# Now sleep, and retry again, in case a race condition meant the two were
# momentarily able to communicate whilst already shutting down
sleep 1m
pytest tests/test_hub_is_ready.py

# Hopefully this works now! If tests still failing output logs
pytest || {
  r=$?
  echo "tests failed"
  display_logs
  exit $r
}

# If tests succeeded show all pods to see if any were restarted
kubectl --namespace $TEST_NAMESPACE get pods
