#!/bin/bash
set -eu

# Install pip
#
# NOTE: pip installs executable packages in ~/.local/bin
#
apt-get -q update
apt-get -q install -y python3-pip


# Install Docker CE
#
# ref: https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script
#
curl -sSL https://get.docker.com | sh
usermod -aG docker vagrant


# Workaround a DNS problem for MacOS running Kubernetes
#
# ref: https://github.com/kubernetes/minikube/issues/2027#issuecomment-338221646
#
# 1. Append two nameserver entries in /etc/hosts
#
cat << EOF > /etc/resolv.conf
nameserver 8.8.4.4
nameserver 8.8.8.8
EOF
# 2. Edit the line starting with 127.0.0.1 in /etc/hosts
#
# "127.0.0.1 localhost" becomes "127.0.0.1 localhost ubuntu1804.localdomain"
#
# NOTE: The sed command below updates the relevant line in the file in place
# -i : --in-place
# -r : --regexp-extended
# -e : --expression
# \1 : anything captured in the first parenthesis
# \\ : "\" escaped for bash with "\\"
#
sed -i -re "s/^(127.0.0.1\\s.+)/\\1 `hostname`/" /etc/hosts


# Make additional setup steps as the vagrant user
su -c "source /home/vagrant/zero-to-jupyterhub-k8s/vagrant-vm-user-setup.sh" vagrant
