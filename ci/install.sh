#!/bin/bash
set -ex

mkdir -p bin

# install nsenter if missing (needed by kube on trusty)
if ! which nsenter; then
  curl -L https://github.com/minrk/git-crypt-bin/releases/download/trusty/nsenter > nsenter
  echo "5652bda3fbea6078896705130286b491b6b1885d7b13bda1dfc9bdfb08b49a2e  nsenter" | shasum -a 256 -c -
  chmod +x nsenter
  sudo mv nsenter /usr/local/bin/
fi

# install kubectl, minikube
# based on https://blog.travis-ci.com/2017-10-26-running-kubernetes-on-travis-ci-with-minikube
echo "installing kubectl"
curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v${KUBE_VERSION}/bin/linux/amd64/kubectl
chmod +x kubectl
mv kubectl bin/

echo "installing minikube"
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v${MINIKUBE_VERSION}/minikube-linux-amd64
chmod +x minikube
mv minikube bin/

echo "starting minikube"
if [[ ${KUBE_VERSION} == 1.9* ]] || [[ ${KUBE_VERSION} == 1.10* ]]; then
  BOOTSTRAPPER=localkube
else
  BOOTSTRAPPER=kubeadm
fi
sudo CHANGE_MINIKUBE_NONE_USER=true $PWD/bin/minikube start --kubernetes-version=v${KUBE_VERSION} --vm-driver=none --bootstrapper=${BOOTSTRAPPER}
minikube update-context

echo "waiting for kubernetes"
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}'
until kubectl get nodes -o jsonpath="$JSONPATH" 2>&1 | grep -q "Ready=True"; do
  sleep 1
done
kubectl get nodes

echo "installing helm"
curl -ssL https://storage.googleapis.com/kubernetes-helm/helm-v${HELM_VERSION}-linux-amd64.tar.gz \
  | tar -xz -C bin --strip-components 1 linux-amd64/helm
chmod +x bin/helm

kubectl --namespace kube-system create sa tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller

echo "waiting for tiller"
kubectl --namespace=kube-system rollout status --watch deployment/tiller-deploy

echo "installing git-crypt"
curl -L https://github.com/minrk/git-crypt-bin/releases/download/0.5.0/git-crypt > bin/git-crypt
echo "46c288cc849c23a28239de3386c6050e5c7d7acd50b1d0248d86e6efff09c61b  bin/git-crypt" | shasum -a 256 -c -
chmod +x bin/git-crypt

echo "installing kubeval"
curl -L https://github.com/garethr/kubeval/releases/download/0.7.1/kubeval-linux-amd64.tar.gz --output bin/kubeval.tar.gz
echo "8259d462bd19e5fc2db2ea304e51ed4db928be4343f6c9530f909dba66e15713  bin/kubeval.tar.gz" | shasum -a 256 -c -
tar xf bin/kubeval.tar.gz -C bin
chmod +x bin/kubeval
