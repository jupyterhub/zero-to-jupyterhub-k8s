#!/bin/bash
set -e
# Install most of the python packages we might use,
# from conda or pip
# NOTE: Please keep package lists alphabetically sorted

# FIXME: Decide on an upgrade policy for these packages
# FIXME: Decide on inclusion policy for these packages

# Basic useful scientific packages
${CONDA_DIR}/bin/conda install --quiet --yes \
            bokeh=0.12* \
            cloudpickle=0.1* \
            cython=0.23* \
            dill=0.2* \
            h5py=2.6* \
            hdf5=1.8.17 \
            matplotlib=1.5* \
            numba=0.23* \
            numexpr=2.6* \
            pandas=0.19* \
            patsy=0.4* \
            scikit-image=0.11* \
            scikit-learn=0.17* \
            scipy=0.17* \
            seaborn=0.7* \
            sqlalchemy=1.0* \
            statsmodels=0.6* \
            sympy=1.0*

# Pre-generate font cache so the user does not see fc-list warning when
# importing datascience. https://github.com/matplotlib/matplotlib/issues/5836
${CONDA_DIR}/bin/python -c 'import matplotlib.pyplot'

${CONDA_DIR}/bin/conda install --quiet --yes numpy=1.11*

# Remove pyqt and qt, since we do not need them with notebooks
${CONDA_DIR}/bin/conda remove --quiet --yes --force qt pyqt

${CONDA_DIR}/bin/conda clean -tipsy
