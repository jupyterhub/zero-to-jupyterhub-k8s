#!/bin/bash
# Install base packages that are generally useful for everyone.
# These should not change often.
apt-get install --yes --quiet --no-install-recommends \
        build-essential \
        bzip2 \
        ca-certificates \
        git \
        locales \
        python3-dev \
        sudo \
        vim \
        wget \
        unzip

apt-get clean
