# The build stage
# ---------------
FROM python:3.9-bullseye as build-stage

# VULN_SCAN_TIME=2022-08-08_05:22:22

WORKDIR /build-stage

# Build wheels for packages that require gcc or other build dependencies and
# lack wheels either for amd64 or aarch64.
#
#   - https://pypi.org/project/psutil/#files, no wheels available as of 5.9.1
#     for aarch64. See https://github.com/giampaolo/psutil/pull/2070.
#
# If you find a dependency here no longer listed in requirements.txt, remove it
# from here as well. The more wheels we build here and copy and then install,
# where the copy and install are separate steps, the larger the final image
# becomes.
#
COPY requirements.txt requirements.txt
RUN pip install build \
 && pip wheel \
        $(cat requirements.txt | grep "psutil==")


# The final stage
# ---------------

FROM python:3.9-slim-bullseye

# VULN_SCAN_TIME=

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

COPY --from=build-stage /build-stage/*.whl /tmp/pre-built-wheels/
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir \
        /tmp/pre-built-wheels/*.whl \
        -r /tmp/requirements.txt

WORKDIR ${HOME}
USER ${NB_USER}

EXPOSE 8888
ENTRYPOINT ["tini", "--"]
CMD ["jupyter", "lab"]
