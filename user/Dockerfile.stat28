FROM gcr.io/data-8/jupyterhub-k8s-user-datahub:48e4097

MAINTAINER Ryan Lovett <rylo@berkeley.edu>

USER root

ADD install-stat28-root.bash /usr/local/sbin/install-stat28-root.bash
RUN /usr/local/sbin/install-stat28-root.bash

USER $NB_USER

ADD install-stat28-nbuser.bash /usr/local/sbin/install-stat28-nbuser.bash
RUN /usr/local/sbin/install-stat28-nbuser.bash
