# This container image will be used by students with JupyterHub
#
# We split things into separate bash scripts that are then run from inside
# the container, rather than super long single lines with && in Docker.
# This is cleaner to understand and maintain in the long run. We trade off
# some docker build time cache for this, but gain in clarity and
# maintainability.
#
# Since we'll be mounting /home/jovyan from a persistent volume, anything
# you add in the docker file under /home/jovyan will never take effect.

FROM gcr.io/data-8/jupyterhub-k8s-user-base:6138fed

MAINTAINER Data Science Infrastructure <ds-inst@berkeley.edu>

USER root

# gdrive executable for nbgdrive extension
RUN wget -q -O /usr/local/bin/gdrive \
  "https://docs.google.com/uc?id=0B3X9GlR6EmbnQ0FtZmJJUXEyRTA&export=download"
RUN chmod +x /usr/local/bin/gdrive

# for geog88
RUN apt-get --yes install libspatialindex-dev libgeos-dev

USER $NB_USER

ADD install-python-packages.bash /usr/local/sbin/install-python-packages.bash
RUN /usr/local/sbin/install-python-packages.bash

ADD install-extensions.bash /usr/local/sbin/install-extensions.bash
RUN /usr/local/sbin/install-extensions.bash

ADD connectors/ecology.bash /usr/local/sbin/connector-ecology.bash
RUN /usr/local/sbin/connector-ecology.bash

ADD connectors/humanities.bash /usr/local/sbin/connector-humanities.bash
RUN /usr/local/sbin/connector-humanities.bash

ADD connectors/child-dev.bash /usr/local/sbin/connector-child-dev.bash
RUN /usr/local/sbin/connector-child-dev.bash

ADD connectors/espm88a.bash /usr/local/sbin/connector-espm88a.bash
RUN /usr/local/sbin/connector-espm88a.bash

ADD connectors/geog88.bash /usr/local/sbin/connector-geog88.bash
RUN /usr/local/sbin/connector-geog88.bash

ADD connectors/cogsci88.bash /usr/local/sbin/connector-cogsci88.bash
RUN /usr/local/sbin/connector-cogsci88.bash

ADD connectors/neuro.bash /usr/local/sbin/connector-neuro.bash
RUN /usr/local/sbin/connector-neuro.bash

ADD install-ds8.bash /usr/local/sbin/install-ds8.bash
RUN /usr/local/sbin/install-ds8.bash
