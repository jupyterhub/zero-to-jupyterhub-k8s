FROM ubuntu:20.04

# VULN_SCAN_HASH=

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      git \
      vim \
      less \
      python3 \
      python3-dev \
      python3-pip \
      python3-setuptools \
      python3-wheel \
      libssl-dev \
      libcurl4-openssl-dev \
      build-essential \
      sqlite3 \
      curl \
      dnsutils \
      && \
    rm -rf /var/lib/apt/lists/*

ARG NB_USER=jovyan
ARG NB_UID=1000
ARG HOME=/home/jovyan

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    --home ${HOME} \
    --force-badname \
    ${NB_USER}

RUN python3 -m pip install --upgrade --no-cache setuptools pip
COPY requirements.txt /tmp/requirements.txt

# NOTE: This is a default and will be overridden by chartpress and the
#       dependencies script using the chartpress.yaml configuration's buildArgs
ARG JUPYTERHUB_VERSION=1.2.2

RUN PYCURL_SSL_LIBRARY=openssl pip3 install --no-cache-dir \
         -r /tmp/requirements.txt \
 && pip3 install --no-cache-dir \
         $(bash -c 'if [[ $JUPYTERHUB_VERSION == "git"* ]]; then \
            echo ${JUPYTERHUB_VERSION}; \
          else \
            echo jupyterhub==${JUPYTERHUB_VERSION}; \
          fi')

WORKDIR /srv/jupyterhub

# So we can actually write a db file here
RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub

# JupyterHub API port
EXPOSE 8081

# when building the dependencies image
# add pip-tools necessary for computing dependencies
# this is not done in production builds by chartpress
ARG PIP_TOOLS=
RUN test -z "$PIP_TOOLS" || pip install --no-cache pip-tools==$PIP_TOOLS

USER ${NB_USER}
CMD ["jupyterhub", "--config", "/etc/jupyterhub/jupyterhub_config.py"]
