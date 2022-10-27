# syntax = docker/dockerfile:1.3
# VULN_SCAN_TIME=2022-08-08_05:22:22


# The build stage
# ---------------
# This stage provides a slimmed /opt/python folder with python and dependencies
# installed.
#
FROM buildpack-deps:22.04 as build-stage

ENV PATH=/opt/python/bin:$PATH

COPY requirements.txt requirements.txt
RUN arch=$(uname -m) \
 && if [ "${arch}" = "x86_64" ]; then arch="64"; fi \
 && wget -qO micromamba.tar.bz2 \
        "https://micro.mamba.pm/api/micromamba/linux-${arch}/latest" \
 && tar -xvjf micromamba.tar.bz2 --strip-components=1 bin/micromamba \
 && rm micromamba.tar.bz2 \
    # Install Python
 && ./micromamba install \
        --root-prefix=/opt/python \
        --prefix=/opt/python \
        --channel=conda-forge \
        --yes \
        "python=3.10" \
        "mamba" \
        "tini" \
 && rm micromamba \
    # Install dependencies
 && pip install --no-cache-dir \
        -r requirements.txt \
    # Cleanup in /opt/python
 && mamba clean --all --force-pkgs-dirs --yes \
 && find /opt/python -type d -name __pycache__ -prune -exec rm -rf {} \;


# The final stage - slim version
# ------------------------------
# This stage is built and published as jupyterhub/k8s-hub-slim. It is meant to
# provide no apt packages besides whats essential.
#
FROM ubuntu:22.04 as slim-stage

ENV DEBIAN_FRONTEND=noninteractive
ARG NB_USER=jovyan \
    NB_UID=1000 \
    HOME=/home/jovyan

RUN adduser --disabled-password \
        --gecos "Default user" \
        --uid ${NB_UID} \
        --home ${HOME} \
        --force-badname \
        ${NB_USER}

COPY --from=build-stage /opt/python /opt/python
ENV PATH=/opt/python/bin:$PATH

WORKDIR /srv/jupyterhub
RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub
USER ${NB_USER}

EXPOSE 8081
ENTRYPOINT ["tini", "--"]
CMD ["jupyterhub", "--config", "/usr/local/etc/jupyterhub/jupyterhub_config.py"]


# The final stage - default version
# ---------------------------------
# We add a few non-critical apt packages on top of the slim version to provide
# some debugging utility for k8s admins.
#
FROM slim-stage

USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        # misc network utilities
        curl \
        dnsutils \
        git \
        # misc other utilities
        less \
        vim \
 && rm -rf /var/lib/apt/lists/*
USER ${NB_USER}
