#!/bin/bash
# This installs and enables notebook extensions
# Always use --sys-prefix when installing or enabling extensions
# This will install them into /opt/conda, which is what we want

# nbserverproxy, for neuro connector and others
${CONDA_DIR}/bin/pip install git+https://github.com/ryanlovett/nbserverproxy.git
${CONDA_DIR}/bin/jupyter serverextension enable --sys-prefix --py nbserverproxy

# ipywidgets!
${CONDA_DIR}/bin/pip install ipywidgets
${CONDA_DIR}/bin/jupyter nbextension enable --sys-prefix --py widgetsnbextension

# nbresuse to show users memory usage
${CONDA_DIR}/bin/pip install git+https://github.com/data-8/nbresuse.git
${CONDA_DIR}/bin/jupyter serverextension enable --sys-prefix --py nbresuse
${CONDA_DIR}/bin/jupyter nbextension install --sys-prefix --py nbresuse
${CONDA_DIR}/bin/jupyter nbextension enable --sys-prefix --py nbresuse

# interact notebook extension
${CONDA_DIR}/bin/pip install git+https://github.com/data-8/nbpuller.git@81fa5ce
#${CONDA_DIR}/bin/pip install git+https://github.com/data-8/nbpuller.git@branch-arg
# FIXME: This should just be in setup.py of the repo
${CONDA_DIR}/bin/pip --no-cache-dir install pytest webargs requests gitpython toolz
${CONDA_DIR}/bin/jupyter serverextension enable --sys-prefix --py nbpuller
${CONDA_DIR}/bin/jupyter nbextension install --sys-prefix --py nbpuller
${CONDA_DIR}/bin/jupyter nbextension enable --sys-prefix --py nbpuller

${CONDA_DIR}/bin/pip install git+https://github.com/data-8/nbgdrive.git@3a98798
${CONDA_DIR}/bin/jupyter serverextension enable --sys-prefix --py nbgdrive
${CONDA_DIR}/bin/jupyter nbextension install --sys-prefix --py nbgdrive
${CONDA_DIR}/bin/jupyter nbextension enable --sys-prefix --py nbgdrive
