#!/bin/bash
# NOTE: The script should be executed from the repo directory

# SCRIPT SUMMARY
# --------------
# 1. Downloads binaries into /bin if they don't already exist
#    - nsenter
#    - minikube $KUBE_VERSION
#    - kubectl  $MINIKUBE_VERSION
#    - helm     $HELM_VERSION
#    - kubeval  $KUBEVAL_VERSION
# 2. (LOCAL DEVELOPMENT ONLY) Setup kubectl and minikube autocomplete

# TODO: setup kubectl's and helm's HOME directories within the repo to avoid
#       influencing installations.

# Set shell options
# -e : Exit immediately if a command exits with a non-zero status.
# -u : Treat unset variables as an error when substituting.
# -x : Print commands and their arguments as they are executed.
set -eux

# Download binaries
# -----------------
# Ensure the bin folder exist
mkdir -p bin

# Ensure nsenter exist as needed by kube on Ubuntu 14.04 (trusty)
if ! which nsenter; then
  echo "installing nsenter"
  curl -sSLo nsenter https://github.com/minrk/git-crypt-bin/releases/download/trusty/nsenter
  echo "5652bda3fbea6078896705130286b491b6b1885d7b13bda1dfc9bdfb08b49a2e  nsenter" | shasum -a 256 -c -
  chmod +x nsenter
  sudo mv nsenter /usr/local/bin/
fi

if ! [ -f bin/kubectl-${KUBE_VERSION} ]; then
  echo "installing kubectl"
  curl -sSLo bin/kubectl-${KUBE_VERSION} https://storage.googleapis.com/kubernetes-release/release/v${KUBE_VERSION}/bin/linux/amd64/kubectl
  chmod +x bin/kubectl-${KUBE_VERSION}
fi
cp bin/kubectl-${KUBE_VERSION} bin/kubectl

if ! [ -f bin/helm-${HELM_VERSION} ]; then
  echo "installing helm"
  curl -sSLo bin/helm-${HELM_VERSION}.tar.gz https://storage.googleapis.com/kubernetes-helm/helm-v${HELM_VERSION}-linux-amd64.tar.gz
  tar --extract --file bin/helm-${HELM_VERSION}.tar.gz --directory bin --strip-components 1 linux-amd64/helm
  rm bin/helm-${HELM_VERSION}.tar.gz
  mv bin/helm bin/helm-${HELM_VERSION}
fi
cp bin/helm-${HELM_VERSION} bin/helm

if ! [ -f bin/minikube-${MINIKUBE_VERSION} ]; then
  echo "installing minikube"
  curl -sSLo bin/minikube-${MINIKUBE_VERSION} https://storage.googleapis.com/minikube/releases/v${MINIKUBE_VERSION}/minikube-linux-amd64
  chmod +x bin/minikube-${MINIKUBE_VERSION}
fi
cp bin/minikube-${MINIKUBE_VERSION} bin/minikube

if ! [ -f bin/kubeval-${KUBEVAL_VERSION} ]; then
  echo "installing kubeval"
  curl -sSLo bin/kubeval-${KUBEVAL_VERSION}.tar.gz https://github.com/garethr/kubeval/releases/download/${KUBEVAL_VERSION}/kubeval-linux-amd64.tar.gz
  tar --extract --file bin/kubeval-${KUBEVAL_VERSION}.tar.gz --directory bin
  rm bin/kubeval-${KUBEVAL_VERSION}.tar.gz
  mv bin/kubeval bin/kubeval-${KUBEVAL_VERSION}
fi
cp bin/kubeval-${KUBEVAL_VERSION} bin/kubeval

if [[ ! -z "${CICD}" ]]; then
  echo "setting up kubectl and minikube autocomplete"
  source <(kubectl completion bash)
  source <(minikube completion bash)
fi
