#!/bin/bash

set -e

# RStudio Server
VERSION=1.0.136
URL="https://download2.rstudio.org/rstudio-server-${VERSION}-amd64.deb"
PACKAGE="$(basename ${URL})"

apt-get -y --quiet --no-install-recommends install \
    gdebi-core \
    lmodern

wget --quiet ${URL}
gdebi --non-interactive ${PACKAGE}
rm ${PACKAGE}

apt-get clean

# RStudio needs to find libR.so
echo /opt/conda/lib/R/lib > /etc/ld.so.conf.d/stat28-conda.conf
ldconfig
