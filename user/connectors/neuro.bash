#!/bin/bash
# conda & pip packages for neuro connector (mark.lescroart)
${CONDA_DIR}/bin/conda install --quiet --yes \
            lxml=3.6.4

${CONDA_DIR}/bin/pip install --egg git+https://github.com/gallantlab/pycortex@data8

${CONDA_DIR}/bin/pip --no-cache-dir install \
            mne==0.13.0 \
            nibabel==2.0.2 \
            tqdm==4.8.4
