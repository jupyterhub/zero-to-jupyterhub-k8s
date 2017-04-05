#!/bin/bash
# This installs notebook and jupyterhub
${CONDA_DIR}/bin/conda install --quiet --yes notebook==4.4.1 ipykernel==4.6.0
${CONDA_DIR}/bin/pip install jupyterhub
