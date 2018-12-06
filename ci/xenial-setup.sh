#!/bin/sh

set -eux

apt-get -q update
apt-get -q install -y socat

# https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce
apt-get -q install -y linux-image-extra-$(uname -r) linux-image-extra-virtual

#DOCKER_DEB=docker-ce_17.09.0~ce-0~ubuntu_amd64.deb
DOCKER_DEB=docker-ce_17.03.2~ce-0~ubuntu-trusty_amd64.deb
curl -O https://download.docker.com/linux/ubuntu/dists/trusty/pool/stable/amd64/$DOCKER_DEB
# dpkg won't install dependencies
dpkg -i $DOCKER_DEB || sudo apt-get install -f -y
docker info

install -o vagrant -g vagrant -d /home/vagrant/bin

# Workaround Minikube DNS problems
# https://github.com/kubernetes/minikube/issues/2027#issuecomment-338221646
cat << EOF > /etc/resolv.conf
nameserver 8.8.4.4
nameserver 8.8.8.8
EOF
sed -i -re "s/^(127.0.0.1\\s.+)/\\1 `hostname`/" /etc/hosts
