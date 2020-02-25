FROM ubuntu:18.04

## NOTE: This is a default and be overridden by chartpress using the
##       chartpress.yaml configuration
ARG JUPYTERHUB_VERSION=1.1.*

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
      $(bash -c 'if [[ $JUPYTERHUB_VERSION == "git"* ]]; then \
        # workaround for https://bugs.launchpad.net/ubuntu/+source/nodejs/+bug/1794589
        echo nodejs=8.10.0~dfsg-2ubuntu0.2 nodejs-dev=8.10.0~dfsg-2ubuntu0.2 npm; \
      fi') \
      && \
    apt-get purge && apt-get clean

ARG NB_USER=jovyan
ARG NB_UID=1000
ARG HOME=/home/jovyan

ENV LANG C.UTF-8

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    --home ${HOME} \
    --force-badname \
    ${NB_USER}

ADD requirements.txt /tmp/requirements.txt
RUN PYCURL_SSL_LIBRARY=openssl pip3 install --no-cache-dir \
         -r /tmp/requirements.txt \
         $(bash -c 'if [[ $JUPYTERHUB_VERSION == "git"* ]]; then \
            echo ${JUPYTERHUB_VERSION}; \
          else \
            echo jupyterhub==${JUPYTERHUB_VERSION}; \
          fi')

# Merge https://github.com/jupyterhub/kubespawner/pull/387 into master and install
RUN cd /tmp && \
    git clone https://github.com/jupyterhub/kubespawner.git && \
    cd kubespawner && \
    git fetch origin "pull/387/head:pr387" && \
    git config user.email "travis-ci@example.org" && \
    git config user.name "Travis CI" && \
    git merge --no-edit pr387 && \
    pip3 install .

WORKDIR /srv/jupyterhub

# So we can actually write a db file here
RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub

# JupyterHub API port
EXPOSE 8081

USER ${NB_USER}
CMD ["jupyterhub", "--config", "/etc/jupyterhub/jupyterhub_config.py"]
