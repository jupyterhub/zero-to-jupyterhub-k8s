FROM jupyter/base-notebook:281505737f8a

# conda/pip/apt install additional packages here, if desired.

# pin jupyterhub to match the Hub version
# set via --build-arg in Makefile
ARG JUPYTERHUB_VERSION=0.8
RUN pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION

