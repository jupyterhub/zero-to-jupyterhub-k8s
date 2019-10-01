#!/bin/sh
set -eu

## Install pip
##
## NOTE: pip installs executable packages in ~/.local/bin
##
apt-get -q update
apt-get -q install -y python3-pip
echo 'PATH=$PATH:~/.local/bin' >> /home/vagrant/.bashrc

## Install Docker CE
##
## ref: https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script
##
curl -sSL https://get.docker.com | sh
usermod -aG docker vagrant

## Put to be downloaded binaries on PATH
echo 'PATH=$PATH:~/zero-to-jupyterhub-k8s/bin' >> /home/vagrant/.bashrc
