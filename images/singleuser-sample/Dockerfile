# The build stage
# ---------------
FROM python:3.9-bullseye as build-stage

# VULN_SCAN_TIME=

WORKDIR /build-stage

# Build wheels for packages that require gcc or other build dependencies and
# lack wheels either for amd64 or aarch64.
COPY requirements.txt requirements.txt
RUN pip wheel -r requirements.txt

# The final stage
# ---------------
FROM python:3.9-slim-bullseye

# VULN_SCAN_TIME=

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    NB_USER=jovyan \
    NB_UID=1000 \
    HOME=/home/jovyan

USER root
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

COPY --from=build-stage /build-stage/*.whl /tmp/pre-built-wheels/
RUN pip install --no-cache-dir /tmp/pre-built-wheels/*.whl

# nbgitpuller is installed in requirements.txt for demo purposes, and this
# enables it to function.
RUN jupyter serverextension enable --py nbgitpuller --sys-prefix

# conda/pip/apt install additional packages here, if desired.

RUN adduser --disabled-password \
        --gecos "Default user" \
        --uid ${NB_UID} \
        --home ${HOME} \
        --force-badname \
        ${NB_USER}

USER $NB_USER

ENTRYPOINT ["tini", "--"]
