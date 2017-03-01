#!/bin/bash

set -e

apt-get -y --quiet --no-install-recommends install \
	apt-transport-https

R_REPO="https://mran.revolutionanalytics.com/snapshot/2017-01-16"
MRAN_KEY="06F90DE5381BA480"
GPG_KEY_SERVER="keyserver.ubuntu.com"
U_CODE="jessie-cran3"

# Configure apt repository for R packages
echo "deb ${R_REPO}/bin/linux/debian ${U_CODE}/" > \
    /etc/apt/sources.list.d/mran.list
gpg --keyserver keyserver.ubuntu.com --recv-keys ${MRAN_KEY}
gpg -a --export ${MRAN_KEY} | apt-key add -
echo -n | openssl s_client -connect mran.revolutionanalytics.com:443 | \
    sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | \
    tee '/usr/local/share/ca-certificates/mran.revolutionanalytics.com.crt'
update-ca-certificates

# Install R
apt-get -q update > /dev/null
apt-get -y --quiet --no-install-recommends install \
        build-essential \
        gcc \
	curl \
        pkg-config \
	libcurl4-openssl-dev \
	libreadline-dev \
	libssl-dev \
	libzmq3-dev \
	r-base r-recommended r-base-dev libopenblas-base \
	r-cran-evaluate \
	r-cran-digest \
	r-cran-testthat

## Define our default R repository
# Use HTTPS for RProfile to prevent an error message in RStudio.
R_REPO_HTTPS=${R_REPO//http:/https:}
echo "options(repos = list(CRAN = '${R_REPO_HTTPS}'))" >> /etc/R/Rprofile.site

# Install R and irkernel
Rscript -e "install.packages(c('crayon', 'formatR', 'devtools', 'uuid', 'rmarkdown', 'repr', 'IRdisplay', 'pbdZMQ', 'vioplot', 'gtools', 'zoo', 'alluvial', 'gpairs', 'quantreg', 'fdrtool', 'gplots', 'hexbin', 'stringr'), repos='${R_REPO}')"
Rscript -e "devtools::install_github('IRkernel/IRkernel')"
Rscript -e "IRkernel::installspec(FALSE)"

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
