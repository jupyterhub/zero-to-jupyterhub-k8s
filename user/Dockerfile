# This container image will be used by students with JupyterHub
# It is organized in the following fashion:
#
#  - Install base packages (useful for everyone) with apt-get
#  - Setup environment variables (particularly locales) that will
#    affect most programs
#  - Setup the user that users will be running as
#  - Install miniconda
#  - Install base packages (notebook, jupyterhub)
#  - Install any packages with specific data needs (such as NLTK)
#  - Install pip packages
#  - Install miniconda packages
#  - Install various notebook extensions
#
# We also split things into separate bash scripts that are
# then run from inside the container, rather than super long
# single lines with && in Docker. This is cleaner to understand
# and maintain in the long run. We trade off some docker build
# time cache for this, but gain in clarity and maintainability.
#
# Since we'll be mounting /home/jovyan from a persistent volume,
# anything you add in the docker file under /home/jovyan will
# never take effect.

FROM debian:jessie

MAINTAINER Derrick Mar <derrickmar1215@berkeley.edu>

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
RUN apt-get update
ADD install-base-apt.bash /usr/local/sbin/install-base-apt.bash
RUN /usr/local/sbin/install-base-apt.bash

# Generate the en_US UTF-8 Locale, and set that to be
# the default locale. Otherwise it'll default to the 8bit C
# locale, and cause problems any time we use characters that
# are not 8-bit ASCII.
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Set the default shell to bash, rather than sh
ENV SHELL /bin/bash

# Configure Environment
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
ENV NB_USER jovyan
ENV NB_UID 1000

# Create a jovyan user with UID 1000. It also automatically
# creates a group with GID 1000 named jovyan
RUN adduser --gecos '' --shell /bin/bash --uid $NB_UID --disabled-password $NB_USER 

# Install conda into $CONDA_DIR, and chown it to $NB_USER
ADD install-conda.bash /usr/local/sbin/install-conda.bash
RUN /usr/local/sbin/install-conda.bash

# Install packages that we use for pdf / publishing related
# things.
ADD install-publishing-apt.bash /usr/local/sbin/install-publishing-apt.bash
RUN /usr/local/sbin/install-publishing-apt.bash

USER $NB_USER

ADD install-base-notebook.bash /usr/local/sbin/install-base-notebook.bash
RUN /usr/local/sbin/install-base-notebook.bash

ADD install-python-packages.bash /usr/local/sbin/install-python-packages.bash
ADD connectors /usr/local/sbin/connectors-setup
RUN /usr/local/sbin/install-python-packages.bash

# Since we put NLTK data in /opt rather than /usr/local,
# we have to explicitly set this
ENV NLTK_DATA ${CONDA_DIR}/nltk

ADD install-extensions.bash /usr/local/sbin/install-extensions.bash
RUN /usr/local/sbin/install-extensions.bash

USER root
# Ensure LaTeX buffer is large enough
RUN echo buf_size=6400000 > /etc/texmf/texmf.d/10data8.cnf
RUN update-texmf

# Download XKCD font for plt.xkcd()
RUN wget -q -P /usr/share/fonts \
  https://github.com/shreyankg/xkcd-desktop/raw/master/Humor-Sans.ttf

# Pre-generate font cache so the user does not see fc-list warning when
# importing datascience. https://github.com/matplotlib/matplotlib/issues/5836
# When run as root, this generates them in /var/cache/fontconfig, and not under $HOME
RUN MPLBACKEND=nbagg python -c 'import matplotlib.pyplot'

#######################################################################

EXPOSE 8888
WORKDIR /home/$NB_USER

CMD jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user="$JPY_USER" \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL

