FROM jupyter/base-notebook:a07573d685a4
# Built from... https://hub.docker.com/r/jupyter/base-notebook/
#               https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile
# Built from... Ubuntu 18.04

# The jupyter/docker-stacks images contains jupyterhub, jupyterlab and the
# jupyterlab-hub extension already.

## NOTE: This is a default and be overridden by chartpress using the
##       chartpress.yaml configuration
ARG JUPYTERHUB_VERSION=1.1.*

# Example install of git and nbgitpuller.
# NOTE: git is already available in the jupyter/minimal-notebook image.
USER root
RUN apt-get update && apt-get install --yes --no-install-recommends \
    dnsutils \
    git \
    iputils-ping \
 && rm -rf /var/lib/apt/lists/*
USER $NB_USER

RUN python -m pip install nbgitpuller \
    $(bash -c 'if [[ $JUPYTERHUB_VERSION == "git"* ]]; then \
       echo ${JUPYTERHUB_VERSION}; \
     else \
       echo jupyterhub==${JUPYTERHUB_VERSION}; \
     fi') && \
    jupyter serverextension enable --py nbgitpuller --sys-prefix

# Uncomment the line below to make nbgitpuller default to start up in JupyterLab
#ENV NBGITPULLER_APP=lab

# conda/pip/apt install additional packages here, if desired.
