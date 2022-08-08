FROM jupyter/base-notebook:latest
# Built from... https://hub.docker.com/r/jupyter/base-notebook/
#               https://github.com/jupyter/docker-stacks/blob/HEAD/base-notebook/Dockerfile
# Built from... Ubuntu 20.04

# VULN_SCAN_TIME=2022-08-08_07:54:05

USER root
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends \
        dnsutils \
        git \
        iputils-ping \
 && rm -rf /var/lib/apt/lists/*
USER $NB_USER

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir \
        -r /tmp/requirements.txt

# nbgitpuller is installed in requirements.txt for demo purposes, and this
# enables it to function.
RUN jupyter serverextension enable --py nbgitpuller --sys-prefix

# conda/pip/apt install additional packages here, if desired.
