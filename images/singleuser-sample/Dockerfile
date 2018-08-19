FROM jupyter/base-notebook:177037d09156
# Built from... https://hub.docker.com/r/jupyter/base-notebook/
#               https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile
# Built from... Ubuntu 16.04

# conda/pip/apt install additional packages here, if desired.

# pin jupyterhub to match the Hub version
# set via --build-arg in Chartpress
ARG JUPYTERHUB_VERSION=0.9.*
RUN pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION
