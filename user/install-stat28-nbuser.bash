#!/bin/bash

# For rpy2.ipython (née rmagic)
${CONDA_DIR}/bin/pip install -U --no-deps \
	rpy2==2.8.5

# nbrsessionproxy notebook extension
${CONDA_DIR}/bin/pip install -U --no-deps \
    git+https://github.com/ryanlovett/nbrsessionproxy.git@v0.1.6
${CONDA_DIR}/bin/jupyter serverextension enable --sys-prefix --py nbrsessionproxy
${CONDA_DIR}/bin/jupyter nbextension install    --sys-prefix --py nbrsessionproxy
${CONDA_DIR}/bin/jupyter nbextension enable     --sys-prefix --py nbrsessionproxy

${CONDA_DIR}/bin/conda clean -tipsy
