# Use latest LTS for this
FROM ubuntu:16.04

RUN apt-get update

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      ca-certificates \
      git \
      libcurl4-openssl-dev \
      libssl-dev \
      python3 \
      python3-dev \
      python3-setuptools \
      python3-pip && \
     apt-get purge && apt-get clean


RUN pip3 install --no-cache-dir \
         jupyterhub==0.7.2 \
         oauthenticator==0.5.1 \
         jupyterhub-dummyauthenticator==0.3.1 \
         jupyterhub-tmpauthenticator==0.2 \
         statsd==3.2.1 \
         pymysql==0.7.11

RUN pip3 --no-cache-dir install git+https://github.com/jupyterhub/kubespawner@8ca8a9f

ADD jupyterhub_config.py /srv/jupyterhub_config.py

WORKDIR /srv/jupyterhub

# JupyterHub API port
EXPOSE 8081

CMD jupyterhub --config /srv/jupyterhub_config.py --no-ssl
