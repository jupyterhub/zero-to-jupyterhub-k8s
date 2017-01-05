#!/bin/bash
# Install apt packages required for various publishing / typestting
# type activities

apt-get install --yes --quiet --no-install-recommends \
        inkscape \
        libsm6 \
        libxrender1 \
        pandoc \
        texlive-fonts-extra \
        texlive-fonts-recommended \
        texlive-generic-recommended \
        texlive-latex-base \
        texlive-latex-extra \
        texlive-xetex

# For matplotlib animation
apt-get install --yes --quiet --no-install-recommends \
        libav-tools

# FIXME: Move this to connector-setup somehow?
# For neuro connector
apt-get install --yes --quiet --no-install-recommends \
        imagemagick

apt-get clean


