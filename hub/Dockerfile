FROM debian:jessie

RUN apt-get update

RUN apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    git \
    libcurl4-openssl-dev \
    libssl-dev \
    python3 \
    python3-dev \
    python3-pip

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir jupyterhub==0.7.2 oauthenticator==0.5.1 jupyterhub-dummyauthenticator==0.1 statsd

RUN pip3 --no-cache-dir install git+https://github.com/jupyterhub/kubespawner@6327b3f

ADD jupyterhub_config.py /srv/jupyterhub_config.py

RUN mkdir -p /srv/jupyterhub
WORKDIR /srv/jupyterhub

# JupyterHub API port
EXPOSE 8081

CMD jupyterhub --config /srv/jupyterhub_config.py --no-ssl
