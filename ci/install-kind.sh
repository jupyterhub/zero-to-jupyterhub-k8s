#!/bin/bash
set -ex

. $PWD/install-lint.sh

# install kubectl, kind
# based on https://blog.travis-ci.com/2017-10-26-running-kubernetes-on-travis-ci-with-minikube
if ! [ -f "bin/kubectl" ]; then
  echo "installing kubectl"
  curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v${KUBE_VERSION}/bin/linux/amd64/kubectl
  chmod +x kubectl
  mv kubectl bin/
fi

if ! [ -f "bin/kind" ]; then
  echo "installing kind"
  curl -Lo kind https://github.com/kubernetes-sigs/kind/releases/download/${KIND_VERSION}/kind-linux-amd64
  chmod +x kind
  mv kind bin/
fi


echo "starting cluster with kind"
$PWD/bin/kind create cluster --image kindest/node:v${KUBE_VERSION}
export KUBECONFIG="$($PWD/bin/kind get kubeconfig-path --name=kind)"

echo "waiting for kubernetes"
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}'
until kubectl get nodes -o jsonpath="$JSONPATH" 2>&1 | grep -q "Ready=True"; do
  sleep 1
done
kubectl get nodes

echo "installing helm"
kubectl --namespace kube-system create sa tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller

echo "waiting for tiller"
kubectl --namespace=kube-system rollout status --watch deployment/tiller-deploy

echo "installing git-crypt"
curl -L https://github.com/minrk/git-crypt-bin/releases/download/0.5.0/git-crypt > bin/git-crypt
echo "46c288cc849c23a28239de3386c6050e5c7d7acd50b1d0248d86e6efff09c61b  bin/git-crypt" | shasum -a 256 -c -
chmod +x bin/git-crypt
