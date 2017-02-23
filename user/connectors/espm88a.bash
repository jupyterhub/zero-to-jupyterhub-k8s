#!/bin/bash
# Install packages & other required bits for the geospatial connector (pfrontiera)
${CONDA_DIR}/bin/conda install --quiet --yes \
            libjpeg-turbo=1.5.1 \
            kealib=1.4.5 \
            gdal=2.0.0 \
            libgdal=2.0.0 \
            pyproj=1.9.5.1 \
            pysal=1.11.1 \
            shapely=1.5.13

${CONDA_DIR}/bin/pip --no-cache-dir install \
            geopy==1.11.0
