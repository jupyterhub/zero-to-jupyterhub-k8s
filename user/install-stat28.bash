#!/bin/bash

set -e

# Install R and irkernel.
${CONDA_DIR}/bin/conda install -c r --quiet --yes \
	r-base=3.3.2 \
	r-irkernel=0.7.1 \
	r-rmarkdown=1.2

${CONDA_DIR}/bin/conda clean -tipsy

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
