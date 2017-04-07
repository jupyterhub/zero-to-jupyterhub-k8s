FROM gcr.io/data-8/jupyterhub-k8s-user-datahub:f0d2b5a

MAINTAINER Ryan Lovett <rylo@berkeley.edu>

USER $NB_USER

ADD install-demo.bash /usr/local/sbin/install-demo.bash
RUN /usr/local/sbin/install-demo.bash
