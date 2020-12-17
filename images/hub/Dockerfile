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

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade --no-cache-dir \
        setuptools \
        pip
RUN PYCURL_SSL_LIBRARY=openssl \
    pip install --no-cache-dir \
        -r /tmp/requirements.txt

# Support overriding a package or two through passed docker --build-args.
# ARG PIP_OVERRIDES="jupyterhub==1.3.0 git+https://github.com/consideratio/kubespawner.git"
ARG PIP_OVERRIDES=
RUN if [[ -n "$PIP_OVERRIDES" ]]; then \
        pip install --no-cache-dir $PIP_OVERRIDES; \
    fi

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
