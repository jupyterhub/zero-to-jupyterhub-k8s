FROM jupyter/singleuser

USER root

# Additional TeX packages for notebooks with unicode characters
RUN apt-get update -q && \
  DEBIAN_FRONTEND=noninteractive apt-get install -q -y \
    texlive-latex-extra \
    texlive-generic-recommended \
    texlive-xetex

# Disable Python 2 kernel
RUN mv /usr/local/share/jupyter/kernels/python2 /var/tmp/

# Download XKCD font for plt.xkcd()
RUN wget -q -P /usr/share/fonts \
  https://github.com/shreyankg/xkcd-desktop/raw/master/Humor-Sans.ttf

# We install each package one by one instead of via requirements.txt because
# periodic changes to that file would invalidate the docker build cache. This
# means that docker would need to repeat later package installations even if we
# were to only change one.
#
# For the similar reasons, we put most frequently changed requirements at the
# bottom.

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

# Pre-generate font cache so the user does not see fc-list warning when
# importing datascience. https://github.com/matplotlib/matplotlib/issues/5836
RUN DEBIAN_FRONTEND=noninteractive apt-get install -q -y \
  libxrender1
RUN python -c 'import matplotlib.pyplot'

# Hack to use xelatex instead of pdflatex
RUN sed -i -e '/ *latex_command =/s/pdflatex/xelatex/' \
  /opt/conda/lib/python*/site-packages/nbconvert/exporters/pdf.py

# For humanities connector ; troland
# models
RUN python -m nltk.downloader -d /usr/local/share/nltk_data averaged_perceptron_tagger
RUN python -m nltk.downloader -d /usr/local/share/nltk_data maxent_ne_chunker
# corpora
RUN python -m nltk.downloader -d /usr/local/share/nltk_data cmudict
RUN python -m nltk.downloader -d /usr/local/share/nltk_data wordnet
RUN python -m nltk.downloader -d /usr/local/share/nltk_data words
#
RUN python -m nltk.downloader -d /usr/local/share/nltk_data punkt

# For geospatial connector ; pfrontiera
RUN pip install geopy==1.11.0
# RUN pip install folium==0.2.1

# For neuro connector ; mark.lescroart
RUN pip install nibabel==2.0.2
RUN pip install mne==0.13.0
RUN pip install tqdm==4.8.4
# For neuro connector ; choldgraf
RUN DEBIAN_FRONTEND=noninteractive apt-get install -q -y \
  imagemagick
#RUN pip install pycortex==0.1.1

# For ds8
RUN pip install okpy==1.6.4
RUN pip install pypandoc==1.2.0
RUN pip install datascience==0.8.2

RUN pip install git+https://github.com/yuvipanda/nbtimetravel.git
RUN jupyter nbextension install --user --py nbtimetravel
RUN jupyter nbextension enable --user --py nbtimetravel

# Ensure LaTeX buffer is large enough
RUN echo buf_size=6400000 > /etc/texmf/texmf.d/10data8.cnf
RUN update-texmf

# Restore atomic intermediate if notebook is invalid.
# This happens when kernels crash on oom conditions.
RUN wget -q -P /tmp http://github.com/jupyter/notebook/commit/6b220c9.patch
# Change into python's site-packages/
RUN cd $(python -c "import site; print(site.getsitepackages()[0])") && \
  patch -p1 < /tmp/6b220c9.patch

# Show memory usage via Yuvi's extension
RUN pip install git+https://github.com/data-8/nbresuse.git
RUN jupyter serverextension enable  --system --py nbresuse
RUN jupyter nbextension     install --system --py nbresuse
RUN jupyter nbextension     enable  --system --py nbresuse

# For child development connector; nishantdesai
RUN pip install pygrowup==0.8.2

# For cogneuro: pycortex
RUN pip install git+https://github.com/ryanlovett/nbserverproxy.git
RUN jupyter serverextension enable --system --py nbserverproxy
RUN pip install --egg git+https://github.com/gallantlab/pycortex@data8

RUN apt-get clean
RUN conda clean --all --yes

USER $NB_USER
