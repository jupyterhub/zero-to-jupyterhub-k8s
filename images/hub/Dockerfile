# syntax = docker/dockerfile:1.3
# VULN_SCAN_TIME=2026-08-31_05:15:06


# The build stage
# ---------------
# This stage is building Python wheels for use in later stages by using a base
# image that has more pre-requisites to do so, such as a C++ compiler.
#
# NOTE: If the image version is updated, also update it in ci/refreeze and
#       singleuser-sample's Dockerfile!
#
FROM python:3.14-trixie as build-stage

# Build wheels
#
# We set pip's cache directory and expose it across build stages via an
# ephemeral docker cache (--mount=type=cache,target=${PIP_CACHE_DIR}). We use
# the same technique for the directory /tmp/wheels.
#
# NOTE: wheel-building stays on plain pip -- uv's `pip` interface has no
#       `wheel` subcommand, so there's nothing to speed up here with uv.
#       The install steps below (which run far more often, on every rebuild
#       that touches requirements.txt) are where uv pays off, so uv is
#       installed and used only in the later stages.
#
COPY requirements.txt requirements.txt
ARG PIP_CACHE_DIR=/tmp/pip-cache
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    pip wheel \
        --wheel-dir=/tmp/wheels \
        # pycurl 7.45.3 has wheels, but they aren't portable
        # https://github.com/pycurl/pycurl/issues/834
        --no-binary pycurl \
        -r requirements.txt \
        # Additional wheels for default-stage. Updates below should be repeated
        # in default-stage.
        #
        py-spy


# The final stage - slim version
# ------------------------------
# This stage is built and published as quay.io/jupyterhub/k8s-hub-slim. It is meant to
# provide no non-essential packages.
#
FROM python:3.14-slim-trixie as slim-stage

# Install uv (static binary, pinned via the official distroless image) to
# speed up installing the wheels built in build-stage compared to pip.
COPY --from=ghcr.io/astral-sh/uv:0.12.11 /uv /uvx /usr/local/bin/

ENV DEBIAN_FRONTEND=noninteractive
ARG NB_USER=jovyan \
    NB_UID=1000 \
    HOME=/home/jovyan
RUN adduser \
        --disabled-password \
        --gecos "Default user" \
        --uid ${NB_UID} \
        --home ${HOME} \
        --force-badname \
        ${NB_USER}

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends \
        # requirement for pycurl
        libcurl4 \
        # requirement for using postgres database
        libpq5 \
        # requirement for using a local sqlite database
        sqlite3 \
        tini \
 && rm -rf /var/lib/apt/lists/*

# install wheels built in the build stage
# --no-index ensures _only_ wheels from the build stage are installed
COPY requirements.txt /tmp/requirements.txt
ARG UV_CACHE_DIR=/tmp/uv-cache
RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    --mount=type=cache,from=build-stage,source=/tmp/wheels,target=/tmp/wheels \
    uv pip install --system \
        --no-index \
        --find-links=/tmp/wheels/ \
        -r /tmp/requirements.txt

WORKDIR /srv/jupyterhub
RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub
USER ${NB_USER}

EXPOSE 8081
ENTRYPOINT ["tini", "--"]
CMD ["jupyterhub", "--config", "/usr/local/etc/jupyterhub/jupyterhub_config.py"]


# The final stage - default version
# ---------------------------------
# We add a few non-critical packages on top of the slim version to provide some
# additional utility.
#
FROM slim-stage as default-stage

USER root

# uv is already present here, inherited from slim-stage.
ARG UV_CACHE_DIR=/tmp/uv-cache
RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    --mount=type=cache,from=build-stage,source=/tmp/wheels,target=/tmp/wheels \
    uv pip install --system \
        --no-index \
        --find-links=/tmp/wheels/ \
        # Updates below should be repeated in build-stage.
        #
        # py-spy is useful for profiling performance of running hubs
        py-spy

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        curl \
        dnsutils \
        git \
        less \
        vim \
 && rm -rf /var/lib/apt/lists/*

USER ${NB_USER}
