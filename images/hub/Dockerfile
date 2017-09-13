FROM ubuntu:17.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      git \
      python3 \
      python3-setuptools \
      libcurl4-openssl-dev \
      build-essential \
      python3-dev \
      libssl-dev \
      npm \
      nodejs-legacy \
      python3-pip && \
     apt-get purge && apt-get clean

ARG NB_USER=jovyan
ARG NB_UID=1000
ARG HOME=/home/jovyan

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    --home ${HOME} \
    --force-badname \
    ${NB_USER}

RUN pip3 install --no-cache-dir \
         git+https://github.com/jupyterhub/jupyterhub@0.8.0b5 \
         statsd==3.2.1 \
         jupyterhub-dummyauthenticator==0.3.1 \
         jupyterhub-tmpauthenticator==0.4 \
         nullauthenticator==1.0 \
         pymysql==0.7.11 \
         psycopg2==2.7.1 \
         pycurl==7.43.0 \
         mwoauth==0.3.2 \
         cryptography==2.0.3

RUN pip3 --no-cache-dir install git+https://github.com/yuvipanda/oauthenticator@0a81eefa04
RUN pip3 --no-cache-dir install git+https://github.com/jupyterhub/kubespawner@fa874329f

ADD jupyterhub_config.py /srv/jupyterhub_config.py
ADD cull_idle_servers.py /usr/local/bin/cull_idle_servers.py

WORKDIR /srv/jupyterhub

# So we can actually write a db file here
RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub

# JupyterHub API port
EXPOSE 8081

USER ${NB_USER}

CMD jupyterhub --config /srv/jupyterhub_config.py
