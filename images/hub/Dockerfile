FROM ubuntu:18.04

ARG JUPYTERHUB_VERSION=0.9.*

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      git \
      libffi-dev \
      libpq-dev \
      libssl-dev \
      python3 \
      python3-dev \
      python3-pip \
      python3-setuptools \
      python3-pycurl \
      build-essential \
      sqlite3 \
      $(bash -c 'if [[ $JUPYTERHUB_VERSION == "git"* ]]; then \
        echo npm; \
      fi') \
      && \
    apt-get purge && apt-get clean

ARG NB_USER=jovyan
ARG NB_UID=1000
ARG HOME=/home/jovyan

ENV LANG C.UTF-8

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    --home ${HOME} \
    --force-badname \
    ${NB_USER}

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir \
         -r /tmp/requirements.txt \
         $(bash -c 'if [[ $JUPYTERHUB_VERSION == "git"* ]]; then \
            echo ${JUPYTERHUB_VERSION}; \
          else \
            echo jupyterhub==${JUPYTERHUB_VERSION}; \
          fi')

ADD jupyterhub_config.py /srv/jupyterhub_config.py

ADD z2jh.py /usr/local/lib/python3.6/dist-packages/z2jh.py
ADD cull_idle_servers.py /usr/local/bin/cull_idle_servers.py

WORKDIR /srv/jupyterhub

# So we can actually write a db file here
RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub

# JupyterHub API port
EXPOSE 8081

USER ${NB_USER}
CMD ["jupyterhub", "--config", "/srv/jupyterhub_config.py"]
