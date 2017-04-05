FROM gcr.io/data-8/jupyterhub-k8s-user-datahub:48e4097

MAINTAINER Ryan Lovett <rylo@berkeley.edu>

USER $NB_USER

ADD install-prob140.bash /usr/local/sbin/install-prob140.bash
RUN /usr/local/sbin/install-prob140.bash
