#!/bin/sh

# Meant to be run from the Vagrantfile allowing

# Set shell options
# -e : Exit immediately if a command exits with a non-zero status.
# -u : Treat unset variables as an error when substituting.
# -x : Print commands and their arguments as they are executed.
set -eux

apt-get --quiet update
apt-get --quiet install --assume-yes socat python3-pip

DOCKER_DEB=docker-ce_18.06.0~ce~3-0~ubuntu_amd64.deb
curl -sSLo $DOCKER_DEB https://download.docker.com/linux/ubuntu/dists/bionic/pool/stable/amd64/$DOCKER_DEB
# dpkg won't install dependencies, so fail and fallback to do it with apt-get
dpkg --install $DOCKER_DEB || sudo apt-get install --fix-broken --assume-yes
docker info

install --owner vagrant --group vagrant --directory /home/vagrant/bin

# Workaround Minikube DNS problems
# https://github.com/kubernetes/minikube/issues/2027#issuecomment-338221646
cat << EOF > /etc/resolv.conf
nameserver 8.8.4.4
nameserver 8.8.8.8
EOF
sed --in-place --regexp-extended --expression "s/^(127.0.0.1\\s.+)/\\1 `hostname`/" /etc/hosts
