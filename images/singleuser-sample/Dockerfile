FROM jupyter/base-notebook:ae885c0a6226

# conda/pip/apt install additional packages here, if desired.

# pin jupyterhub to match the Hub version
# set via --build-arg in Makefile
ARG JUPYTERHUB_VERSION=0.7.2
RUN pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION
