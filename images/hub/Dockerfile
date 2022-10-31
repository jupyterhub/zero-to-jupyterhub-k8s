# syntax = docker/dockerfile:1.3
# The build stage
# ---------------
FROM python:3.9-bullseye as build-stage

# VULN_SCAN_TIME=2022-10-31_05:34:04

WORKDIR /build-stage

# set pip's cache directory using this environment variable, and use
# ARG instead of ENV to ensure its only set when the image is built
ARG PIP_CACHE_DIR=/tmp/pip-cache

# Build wheels
# These are mounted into the final image for installation
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    pip install build \
 && pip wheel -r requirements.txt


# The final stage
# ---------------
FROM python:3.9-slim-bullseye

ARG NB_USER=jovyan
ARG NB_UID=1000
ARG HOME=/home/jovyan

ENV DEBIAN_FRONTEND=noninteractive

RUN adduser --disabled-password \
        --gecos "Default user" \
        --uid ${NB_UID} \
        --home ${HOME} \
        --force-badname \
        ${NB_USER}

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        # misc network utilities
        curl \
        dnsutils \
        git \
        # misc other utilities
        less \
        vim \
        # requirement for pycurl
        libcurl4 \
        # requirement for using a local sqlite database
        sqlite3 \
        tini \
 && rm -rf /var/lib/apt/lists/*

# set pip's cache directory using this environment variable, and use
# ARG instead of ENV to ensure its only set when the image is built
ARG PIP_CACHE_DIR=/tmp/pip-cache

# install wheels built in the build-stage
COPY requirements.txt /tmp/requirements.txt
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    --mount=type=cache,from=build-stage,source=/build-stage,target=/tmp/wheels \
    pip install \
        --find-links=/tmp/wheels/ \
        -r /tmp/requirements.txt

WORKDIR /srv/jupyterhub
RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub
USER ${NB_USER}

EXPOSE 8081
ENTRYPOINT ["tini", "--"]
CMD ["jupyterhub", "--config", "/usr/local/etc/jupyterhub/jupyterhub_config.py"]
