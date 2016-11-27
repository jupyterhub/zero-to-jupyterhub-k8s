FROM debian:jessie

MAINTAINER Derrick Mar <derrickmar1215@berkeley.edu>

USER root

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive
RUN REPO=http://cdn-fastly.deb.debian.org \
 && echo "deb $REPO/debian jessie main\ndeb $REPO/debian-security jessie/updates main" > /etc/apt/sources.list \
 && apt-get update && apt-get -yq dist-upgrade \
 && apt-get install -yq --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Housekeeping
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Configure Environment
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
ENV SHELL /bin/bash
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV NB_USER jovyan
ENV NB_UID 1000

# Create jovyan user with UID=1000 and in the 'users' group
RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    mkdir -p $CONDA_DIR && \
    chown $NB_USER $CONDA_DIR

USER $NB_USER

# Setup jovyan home directory
RUN mkdir /home/$NB_USER/work && \
    mkdir /home/$NB_USER/.jupyter && \
    echo "cacert=/etc/ssl/certs/ca-certificates.crt" > /home/$NB_USER/.curlrc

# INSTALL CONDA AS JOVYAN
RUN cd /tmp && \
    mkdir -p $CONDA_DIR && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.1.11-Linux-x86_64.sh && \
    echo "efd6a9362fc6b4085f599a881d20e57de628da8c1a898c08ec82874f3bad41bf *Miniconda3-4.1.11-Linux-x86_64.sh" | sha256sum -c - && \
    /bin/bash Miniconda3-4.1.11-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-4.1.11-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda install --quiet --yes conda==4.1.11 && \
    $CONDA_DIR/bin/conda config --system --add channels conda-forge && \
    $CONDA_DIR/bin/conda config --system --set auto_update_conda false && \
    conda clean -tipsy

COPY conda_packages.txt /tmp/conda_packages.txt

# INSTALL CONDA PACKAGES
# Remove pyqt and qt pulled in for matplotlib since we're only ever going to
# use notebook-friendly backends in these images
RUN conda install --quiet --yes --file /tmp/conda_packages.txt && \
    conda remove --quiet --yes --force qt pyqt && \
    conda clean -tipsy

RUN conda install --yes numpy==1.11.0

# INSTALL NOTEBOOK AS JOVYAN
RUN conda install --quiet --yes \
    'notebook=4.2*' \
    && conda clean -tipsy

# INSTALL HUB AS JOVYAN
# Install JupyterHub to get the jupyterhub-singleuser startup script
# Use --pre to use 0.7 version
RUN pip install --no-cache-dir --pre jupyterhub

USER root

# NLTK
RUN python -m nltk.downloader -d /usr/local/share/nltk_data \
    averaged_perceptron_tagger \
    maxent_ne_chunker \
    cmudict \
    wordnet \
    words \
    punkt

# INSTALL ADDITIONAL PACKAGES WITH PIP
COPY pip_packages.txt /tmp/pip_packages.txt
RUN pip install -r /tmp/pip_packages.txt

COPY apt_get_packages.txt /tmp/apt_get_packages.txt
RUN apt-get update && apt-get install -yq \
    $(grep -vE "^\s*#" /tmp/apt_get_packages.txt | tr "\n" " ") \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# For cogneuro: pycortex
RUN pip install git+https://github.com/ryanlovett/nbserverproxy.git
RUN pip install --egg git+https://github.com/gallantlab/pycortex@data8

####################### NOTEBOOK EXTENSIONS  ###########################
RUN jupyter serverextension enable --system --py nbserverproxy

# Activate ipywidgets extension in the environment that runs the notebook server
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix

# TODO: Ask Yuvi to optimize nbtimetravel for large notebooks
RUN pip install git+https://github.com/yuvipanda/nbtimetravel.git
RUN jupyter nbextension install --system --py nbtimetravel
RUN jupyter nbextension enable --system --py nbtimetravel

# Show memory usage via Yuvi's extension
RUN pip install git+https://github.com/data-8/nbresuse.git
RUN jupyter serverextension enable  --system --py nbresuse
RUN jupyter nbextension     install --system --py nbresuse
RUN jupyter nbextension     enable  --system --py nbresuse
#######################################################################

################################ MISC #################################
# Hack to use xelatex instead of pdflatex
RUN sed -i -e '/ *latex_command =/s/pdflatex/xelatex/' \
  /opt/conda/lib/python*/site-packages/nbconvert/exporters/pdf.py

# Ensure LaTeX buffer is large enough
RUN echo buf_size=6400000 > /etc/texmf/texmf.d/10data8.cnf
RUN update-texmf

# Download XKCD font for plt.xkcd()
RUN wget -q -P /usr/share/fonts \
  https://github.com/shreyankg/xkcd-desktop/raw/master/Humor-Sans.ttf

# Pre-generate font cache so the user does not see fc-list warning when
# importing datascience. https://github.com/matplotlib/matplotlib/issues/5836
# RUN python -c 'import matplotlib.pyplot'

# Restore atomic intermediate if notebook is invalid.
# This happens when kernels crash on oom conditions.
RUN wget -q -P /tmp http://github.com/jupyter/notebook/commit/6b220c9.patch
# Change into python's site-packages/
RUN cd $(python -c "import site; print(site.getsitepackages()[0])") && \
  patch -p1 < /tmp/6b220c9.patch

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.10.0/tini && \
    echo "1361527f39190a7338a0b434bd8c88ff7233ce7b9a4876f3315c22fce7eca1b0 *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini
#######################################################################

RUN pip install git+https://github.com/data-8/nbinteract.git
RUN pip --no-cache-dir install pytest webargs requests gitpython toolz
RUN jupyter serverextension enable --system --py nbinteract
RUN jupyter nbextension install --system --py nbinteract
RUN jupyter nbextension enable --system --py nbinteract

# CLEANUP
RUN apt-get clean
RUN conda clean --all --yes

EXPOSE 8888
WORKDIR /home/$NB_USER/work

USER $NB_USER

ENTRYPOINT ["tini", "--"]

CMD jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user="$JPY_USER" \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL

