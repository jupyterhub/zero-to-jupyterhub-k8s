#!/bin/bash

set -e

VERSION=1.0.136
URL="https://download2.rstudio.org/rstudio-server-${VERSION}-amd64.deb"
PACKAGE="$(basename ${URL})"

apt-get update
apt-get -y --quiet --no-install-recommends install \
    gdebi-core \
    r-base \
    r-base-dev \
    libopenblas-base

wget --quiet ${URL}
gdebi --non-interactive ${PACKAGE}
rm ${PACKAGE}

apt-get clean
