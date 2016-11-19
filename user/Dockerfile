# CHECKPOINT 2
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

# apt-get utility
# Install all OS dependencies for fully functional notebook server
RUN apt-get update && apt-get install -yq --no-install-recommends \
    git \
    vim \
    jed \
    emacs \
    build-essential \
    python-dev \
    unzip \
    libsm6 \
    pandoc \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    libxrender1 \
    inkscape \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# INSTALL CONDA
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

# INSTALL CONDA PACKAGES
# Install Python 3 packages
# Remove pyqt and qt pulled in for matplotlib since we're only ever going to
# use notebook-friendly backends in these images
RUN conda install --quiet --yes \
    'nomkl' \
    'ipywidgets=5.2*' \
    'pandas=0.19*' \
    'numexpr=2.6*' \
    'matplotlib=1.5*' \
    'scipy=0.17*' \
    'seaborn=0.7*' \
    'scikit-learn=0.17*' \
    'scikit-image=0.11*' \
    'sympy=1.0*' \
    'cython=0.23*' \
    'patsy=0.4*' \
    'statsmodels=0.6*' \
    'cloudpickle=0.1*' \
    'dill=0.2*' \
    'numba=0.23*' \
    'bokeh=0.11*' \
    'sqlalchemy=1.0*' \
    'hdf5=1.8.17' \
    'h5py=2.6*' && \
    conda remove --quiet --yes --force qt pyqt && \
    conda clean -tipsy

# MATPLOT LIB CONFIG
# libav-tools for matplotlib anim
RUN apt-get update && \
    apt-get install -y --no-install-recommends libav-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# INSTALL NOTEBOOK
RUN conda install --quiet --yes \
    'notebook=4.2*' \
    && conda clean -tipsy

# INSTALL HUB
# Install JupyterHub to get the jupyterhub-singleuser startup script
RUN pip install --no-cache-dir --pre jupyterhub

# CONNECTOR COURSES PACKAGES
# For reproducibility
RUN conda install --yes ipython==4.2.0
RUN conda install --yes jupyter_client==4.3.0
RUN conda install --yes matplotlib==1.5.1
RUN conda install --yes nbconvert==4.2.0
RUN conda install --yes notebook==4.2.1
RUN conda install --yes numpy==1.11.0
RUN conda install --yes pip==8.1.2
RUN conda install --yes pyzmq==15.2.0
RUN conda install --yes requests==2.10.0
RUN conda install --yes scipy==0.17.1
RUN conda install --yes terminado==0.6
RUN conda install --yes traitlets==4.2.1

# For geospatial connector ; pfrontiera
RUN conda install --yes gdal==2.0.0 libgdal==2.0.0
RUN conda install --yes pyproj==1.9.5.1
RUN conda install --yes pysal==1.11.1
RUN conda install --yes shapely==1.5.13

# For ecology connector ; cboettig
RUN conda install --yes numexpr==2.6.0
RUN conda install --yes psycopg2==2.6.1

# For humanities connector ; troland
RUN conda install --yes gensim==0.12.4
RUN conda install --yes nltk==3.2.1

# For neuro connector ; mark.lescroart
RUN conda install --yes lxml==3.6.4

# For humanities connector ; troland
# models
RUN python -m nltk.downloader -d /usr/local/share/nltk_data averaged_perceptron_tagger
RUN python -m nltk.downloader -d /usr/local/share/nltk_data maxent_ne_chunker

# corpora
RUN python -m nltk.downloader -d /usr/local/share/nltk_data cmudict
RUN python -m nltk.downloader -d /usr/local/share/nltk_data wordnet
RUN python -m nltk.downloader -d /usr/local/share/nltk_data words
RUN python -m nltk.downloader -d /usr/local/share/nltk_data punkt

# For geospatial connector ; pfrontiera
RUN pip install geopy==1.11.0

# For neuro connector ; mark.lescroart
RUN pip install nibabel==2.0.2
RUN pip install mne==0.13.0
RUN pip install tqdm==4.8.4

# For neuro connector ; choldgraf
RUN apt-get update -q && \
  DEBIAN_FRONTEND=noninteractive apt-get install -q -y \
    imagemagick

# For child development connector; nishantdesai
RUN pip install pygrowup==0.8.2

# For cogneuro: pycortex
RUN pip install git+https://github.com/ryanlovett/nbserverproxy.git
RUN jupyter serverextension enable --system --py nbserverproxy
RUN pip install --egg git+https://github.com/gallantlab/pycortex@data8

#DS8
RUN pip install okpy==1.6.4
RUN pip install pypandoc==1.2.0
RUN pip install datascience==0.8.2

# TEX
# Additional TeX packages for notebooks with unicode characters
RUN apt-get update -q && \
  DEBIAN_FRONTEND=noninteractive apt-get install -q -y \
    texlive-latex-extra \
    texlive-generic-recommended \
    texlive-xetex

# Hack to use xelatex instead of pdflatex
RUN sed -i -e '/ *latex_command =/s/pdflatex/xelatex/' \
  /opt/conda/lib/python*/site-packages/nbconvert/exporters/pdf.py

# Ensure LaTeX buffer is large enough
RUN echo buf_size=6400000 > /etc/texmf/texmf.d/10data8.cnf
RUN update-texmf

# FONTS
# Download XKCD font for plt.xkcd()
RUN wget -q -P /usr/share/fonts \
  https://github.com/shreyankg/xkcd-desktop/raw/master/Humor-Sans.ttf

# Pre-generate font cache so the user does not see fc-list warning when
# importing datascience. https://github.com/matplotlib/matplotlib/issues/5836
RUN DEBIAN_FRONTEND=noninteractive apt-get install -q -y \
  libxrender1
RUN python -c 'import matplotlib.pyplot'


# NOTEBOOK EXTENSIONS
# Activate ipywidgets extension in the environment that runs the notebook server
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix

RUN pip install git+https://github.com/yuvipanda/nbtimetravel.git
RUN jupyter nbextension install --system --py nbtimetravel
RUN jupyter nbextension enable --system --py nbtimetravel

# Show memory usage via Yuvi's extension
RUN pip install git+https://github.com/data-8/nbresuse.git
RUN jupyter serverextension enable  --system --py nbresuse
RUN jupyter nbextension     install --system --py nbresuse
RUN jupyter nbextension     enable  --system --py nbresuse

# MISC
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

# CLEANUP
RUN apt-get clean
RUN conda clean --all --yes

EXPOSE 8888

CMD jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user="$JPY_USER" \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL

