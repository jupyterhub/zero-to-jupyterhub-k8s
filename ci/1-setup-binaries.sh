#!/bin/bash

# SCRIPT SUMMARY
# --------------
# 1. Downloads binaries into /ci/bin
#    - nsenter
#    - minikube $KUBE_VERSION
#    - kubectl  $MINIKUBE_VERSION
#    - helm     $HELM_VERSION
#    - kubeval  $KUBEVAL_VERSION

# NOTE: The script should be executed from the repo directory

# Set shell options
# -e : Exit immediately if a command exits with a non-zero status.
# -u : Treat unset variables as an error when substituting.
# -x : Print commands and their arguments as they are executed.
set -eux

# Download binaries
# -----------------
# Ensure the bin folder exist
mkdir -p ci/bin

# Ensure nsenter exist as needed by kube on Ubuntu 14.04 (trusty)
if ! which nsenter; then
  echo "installing nsenter"
  curl -sSLo nsenter https://github.com/minrk/git-crypt-bin/releases/download/trusty/nsenter
  echo "5652bda3fbea6078896705130286b491b6b1885d7b13bda1dfc9bdfb08b49a2e  nsenter" | shasum -a 256 -c -
  chmod +x nsenter
  sudo mv nsenter /usr/local/bin/
fi

echo "installing kubectl"
if ! [ -f ci/bin/kubectl-${KUBE_VERSION} ]; then
  curl -sSLo ci/bin/kubectl-${KUBE_VERSION} https://storage.googleapis.com/kubernetes-release/release/v${KUBE_VERSION}/bin/linux/amd64/kubectl
  chmod +x ci/bin/kubectl-${KUBE_VERSION}
fi
cp ci/bin/kubectl-${KUBE_VERSION} ci/bin/kubectl

echo "installing helm"
if ! [ -f ci/bin/helm-${HELM_VERSION} ]; then
  curl -sSLo ci/bin/helm-${HELM_VERSION}.tar.gz https://storage.googleapis.com/kubernetes-helm/helm-v${HELM_VERSION}-linux-amd64.tar.gz
  tar --extract --file ci/bin/helm-${HELM_VERSION}.tar.gz --directory ci/bin --strip-components 1 linux-amd64/helm
  rm ci/bin/helm-${HELM_VERSION}.tar.gz
  mv ci/bin/helm ci/bin/helm-${HELM_VERSION}
fi
cp ci/bin/helm-${HELM_VERSION} ci/bin/helm

echo "installing minikube"
if ! [ -f ci/bin/minikube-${MINIKUBE_VERSION} ]; then
  curl -sSLo ci/bin/minikube-${MINIKUBE_VERSION} https://storage.googleapis.com/minikube/releases/v${MINIKUBE_VERSION}/minikube-linux-amd64
  chmod +x ci/bin/minikube-${MINIKUBE_VERSION}
fi
cp ci/bin/minikube-${MINIKUBE_VERSION} ci/bin/minikube

echo "installing kubeval"
if ! [ -f ci/bin/kubeval-${KUBEVAL_VERSION} ]; then
  curl -sSLo ci/bin/kubeval-${KUBEVAL_VERSION}.tar.gz https://github.com/garethr/kubeval/releases/download/${KUBEVAL_VERSION}/kubeval-linux-amd64.tar.gz
  tar --extract --file ci/bin/kubeval-${KUBEVAL_VERSION}.tar.gz --directory ci/bin
  rm ci/bin/kubeval-${KUBEVAL_VERSION}.tar.gz
  mv ci/bin/kubeval ci/bin/kubeval-${KUBEVAL_VERSION}
fi
cp ci/bin/kubeval-${KUBEVAL_VERSION} ci/bin/kubeval
