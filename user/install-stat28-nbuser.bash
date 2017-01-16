#!/bin/bash

# Install R and irkernel.
${CONDA_DIR}/bin/conda install -c r --quiet --yes \
        r-base=3.3.2 \
        r-irkernel=0.7.1 \
        r-rmarkdown=1.2

# nbrsessionproxy notebook extension
${CONDA_DIR}/bin/pip install -U --no-deps \
    git+https://github.com/ryanlovett/nbrsessionproxy.git@v0.1.5
${CONDA_DIR}/bin/jupyter serverextension enable --sys-prefix --py nbrsessionproxy
${CONDA_DIR}/bin/jupyter nbextension install    --sys-prefix --py nbrsessionproxy
${CONDA_DIR}/bin/jupyter nbextension enable     --sys-prefix --py nbrsessionproxy

${CONDA_DIR}/bin/conda clean -tipsy
