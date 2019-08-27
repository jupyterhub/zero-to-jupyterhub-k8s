#!/bin/bash
set -ex

# https://github.com/moby/moby/issues/39120
sudo cat /etc/docker/daemon.json
echo '{"mtu": 1460}' | sudo dd of=/etc/docker/daemon.json
sudo systemctl restart docker
docker ps -a
