#!/bin/bash
# DS8 specific packages
${CONDA_DIR}/bin/pip --no-cache-dir install \
            datascience==0.9.3 \
            nbgrader==0.4.0rc1 \
            okpy==1.9.5 \
            pypandoc==1.2.0 \
            git+https://github.com/choldgraf/connectortools.git@86ea3e3 \
            ;
