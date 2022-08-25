FROM python:3.9-slim-bullseye

# VULN_SCAN_TIME=

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    NB_USER=jovyan \
    NB_UID=1000 \
    HOME=/home/jovyan

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends \
        ca-certificates \
        dnsutils \
        git \
        locales \
        iputils-ping \
        tini \
 && rm -rf /var/lib/apt/lists/* \
 && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen

RUN adduser --disabled-password \
        --gecos "Default user" \
        --uid ${NB_UID} \
        --home ${HOME} \
        --force-badname \
        ${NB_USER}

USER $NB_USER

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# nbgitpuller is installed in requirements.txt for demo purposes, and this
# enables it to function.
RUN jupyter serverextension enable --py nbgitpuller --sys-prefix

ENTRYPOINT ["tini", "--"]
