#!/bin/bash

${CONDA_DIR}/bin/pip --no-cache-dir install \
    fiona==1.7.4 \
    mplleaflet==0.0.5 \
    ;

${CONDA_DIR}/bin/conda install --quiet --yes \
    libspatialindex=1.8.5 \
    rtree=0.8.3 \
    geopandas=0.2.1
