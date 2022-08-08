# The build stage
# ---------------
FROM python:3.9-bullseye as build-stage

# VULN_SCAN_TIME=2022-08-08_05:22:22

WORKDIR /build-stage

# Build wheels for packages that require gcc or other build dependencies and
# lack wheels either for amd64 or aarch64.
#
#   - https://pypi.org/project/pycurl/#files, no wheels available as of 7.45.1.
#     See https://github.com/pycurl/pycurl/issues/738.
#   - https://pypi.org/project/ruamel.yaml.clib/#files, no aarch64 wheels
#     available as of 0.2.6. See
#     https://sourceforge.net/p/ruamel-yaml-clib/tickets/4/.
#
# If you find a dependency here no longer listed in requirements.txt, remove it
# from here as well. The more wheels we build here and copy and then install,
# where the copy and install are separate steps, the larger the final image
# becomes.
#
COPY requirements.txt requirements.txt
RUN pip install build \
 && pip wheel \
        $(cat requirements.txt | grep "pycurl==") \
        $(cat requirements.txt | grep "ruamel-yaml-clib==")


# The final stage
# ---------------
FROM python:3.9-slim-bullseye

ARG NB_USER=jovyan
ARG NB_UID=1000
ARG HOME=/home/jovyan
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8

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
 && rm -rf /var/lib/apt/lists/*

RUN if [ "$(uname -m)" = x86_64 ]; then ARCH=amd64; fi; \
    if [ "$(uname -m)" = aarch64 ]; then ARCH=arm64; fi; \
    curl -sSLo /tini "https://github.com/krallin/tini/releases/download/v0.19.0/tini-$ARCH" \
 && chmod +x /tini

COPY --from=build-stage /build-stage/*.whl /tmp/pre-built-wheels/
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir \
        /tmp/pre-built-wheels/*.whl \
        -r /tmp/requirements.txt

WORKDIR /srv/jupyterhub
RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub
USER ${NB_USER}

EXPOSE 8081
ENTRYPOINT ["/tini", "--"]
CMD ["jupyterhub", "--config", "/usr/local/etc/jupyterhub/jupyterhub_config.py"]
