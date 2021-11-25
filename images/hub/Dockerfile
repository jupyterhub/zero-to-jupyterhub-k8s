FROM ubuntu:20.04

# VULN_SCAN_TIME=2021-11-25_01:05:45

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8

# psycopg2-binary in requirements.txt is not compiled for linux/arm64
# TODO: Use build stages to compile psycopg2-binary separately instead of
# bloating the image size
RUN EXTRA_APT_PACKAGES=; \
    if [ `uname -m` != 'x86_64' ]; then EXTRA_APT_PACKAGES=libpq-dev; fi; \
    apt-get update && \
    apt-get upgrade -y && \
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
      $EXTRA_APT_PACKAGES \
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
RUN if test -n "$PIP_OVERRIDES"; then \
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
CMD ["jupyterhub", "--config", "/usr/local/etc/jupyterhub/jupyterhub_config.py"]
