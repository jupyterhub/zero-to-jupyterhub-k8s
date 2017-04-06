#!/bin/bash

${CONDA_DIR}/bin/pip --no-cache-dir install \
    fiona==1.7.4 \
    mplleaflet==0.0.5 \
    rtree==0.8.3 \
    geopandas==0.2.1 \
    netCDF4==1.2.7 \
    nco==0.0.3 \
    https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz \
    ;
# FIXME: Install basemap from pip once https://github.com/matplotlib/basemap/issues/251 is fixed
