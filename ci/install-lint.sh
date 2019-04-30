#!/bin/bash
set -ex

mkdir -p bin

# nsenter is included on xenial

# install socat (required by helm)
sudo apt-get update && sudo apt-get install -y socat

echo "installing kubeval"
if ! [ -f bin/kubeval-${KUBEVAL_VERSION} ]; then
  curl -sSLo bin/kubeval-${KUBEVAL_VERSION}.tar.gz https://github.com/garethr/kubeval/releases/download/${KUBEVAL_VERSION}/kubeval-linux-amd64.tar.gz
  tar --extract --file bin/kubeval-${KUBEVAL_VERSION}.tar.gz --directory bin
  rm bin/kubeval-${KUBEVAL_VERSION}.tar.gz
  mv bin/kubeval bin/kubeval-${KUBEVAL_VERSION}
fi
cp bin/kubeval-${KUBEVAL_VERSION} bin/kubeval

echo "installing helm"
curl -ssL https://storage.googleapis.com/kubernetes-helm/helm-v${HELM_VERSION}-linux-amd64.tar.gz \
  | tar -xz -C bin --strip-components 1 linux-amd64/helm
chmod +x bin/helm
