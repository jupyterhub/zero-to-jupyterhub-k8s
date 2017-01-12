#!/bin/bash
# This installs notebook and jupyterhub
${CONDA_DIR}/bin/conda install --quiet --yes notebook
${CONDA_DIR}/bin/pip install jupyterhub
