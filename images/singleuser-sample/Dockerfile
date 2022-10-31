# syntax = docker/dockerfile:1.3
# The build stage
# ---------------
FROM python:3.9-bullseye as build-stage

# VULN_SCAN_TIME=2022-10-31_05:34:56

WORKDIR /build-stage

# set pip's cache directory using this environment variable, and use
# ARG instead of ENV to ensure its only set when the image is built
ARG PIP_CACHE_DIR=/tmp/pip-cache

# These are mounted into the final image for installation
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    pip install build \
 && pip wheel -r requirements.txt


# The final stage
# ---------------

FROM python:3.9-slim-bullseye

# VULN_SCAN_TIME=2022-10-31_05:34:56

ENV DEBIAN_FRONTEND=noninteractive \
    NB_USER=jovyan \
    NB_UID=1000 \
    HOME=/home/jovyan

RUN adduser --disabled-password \
        --gecos "Default user" \
        --uid ${NB_UID} \
        --home ${HOME} \
        --force-badname \
        ${NB_USER}

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends \
        ca-certificates \
        dnsutils \
        iputils-ping \
        tini \
        # requirement for nbgitpuller
        git \
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

WORKDIR ${HOME}
USER ${NB_USER}

EXPOSE 8888
ENTRYPOINT ["tini", "--"]
CMD ["jupyter", "lab"]
