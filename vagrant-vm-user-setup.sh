#!/bin/bash

# Enter the mounted repo folder
cd ~/zero-to-jupyterhub-k8s


# Install Python dependencies and put them on PATH
pip3 install -r dev-requirements.txt
pip3 install -r doc/doc-requirements.txt
echo 'PATH=$PATH:~/.local/bin' >> ~/.bashrc


# Install binaries and put them on PATH
. ci/common --setup
echo 'PATH=$PATH:~/zero-to-jupyterhub-k8s/bin' >> ~/.bashrc


# Setup autocompletion
echo 'source <(kubectl completion bash)' >>~/.bashrc
echo 'source <(helm completion bash)' >>~/.bashrc
