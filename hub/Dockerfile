FROM debian:jessie

RUN apt-get update
RUN apt-get install -y --no-install-recommends python3 python3-pip ca-certificates git npm

RUN pip3 install --upgrade pip

# bower requires 'node'
# https://lists.debian.org/debian-devel-announce/2012/07/msg00002.html
RUN ln -s /usr/bin/nodejs /usr/local/bin/node

RUN pip3 install --no-cache-dir git+https://github.com/jupyterhub/jupyterhub@master
RUN pip3 install oauthenticator==0.4.*

RUN pip3 --no-cache-dir install git+https://github.com/jupyterhub/kubespawner

ADD jupyterhub_config.py /srv/jupyterhub_config.py

WORKDIR /srv/jupyterhub

# JupyterHub API port
EXPOSE 8081

CMD jupyterhub --config /srv/jupyterhub_config.py --no-ssl
