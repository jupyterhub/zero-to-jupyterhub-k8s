#!/bin/bash
# conda & pip packages for neuro connector (mark.lescroart)
${CONDA_DIR}/bin/conda install --quiet --yes \
	lxml==3.7.2 \
	nibabel==2.1.0 \
	tqdm==4.11.0

${CONDA_DIR}/bin/pip --no-cache-dir install \
	mne==0.13.1

# pycortex can't be installed from the repository at the moment
# ${CONDA_DIR}/bin/pip install git+https://github.com/gallantlab/pycortex@data8

# Installs the cortex library
git clone https://github.com/gallantlab/pycortex
cd pycortex
git checkout data8
${CONDA_DIR}/bin/python setup.py install
