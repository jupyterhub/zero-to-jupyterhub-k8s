#!/bin/sh

# NOTE: Meant to be run indirectly through `vagrant up` in the ci folder
# WARNING: Comes with Python 3.4 and failing to install dev-requirements.txt

# Set shell options
# -e : Exit immediately if a command exits with a non-zero status.
# -u : Treat unset variables as an error when substituting.
# -x : Print commands and their arguments as they are executed.
set -eux

apt-get --quiet update
apt-get --quiet install --assume-yes socat
apt-get --quiet install --assume-yes --upgrade python3-pip

# https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce
apt-get --quiet install --assume-yes linux-image-extra-$(uname --kernel-release) linux-image-extra-virtual

DOCKER_DEB=docker-ce_17.03.2~ce-0~ubuntu-trusty_amd64.deb
curl -sL --output $DOCKER_DEB https://download.docker.com/linux/ubuntu/dists/trusty/pool/stable/amd64/$DOCKER_DEB
# dpkg won't install dependencies
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
