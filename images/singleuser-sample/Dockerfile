FROM ubuntu:17.04

RUN apt-get update && \
    apt-get install --yes --no-install-recommends python3 python3-venv && \
    apt-get purge && apt-get clean

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan

RUN mkdir -p /srv/venv && chown -R jovyan:jovyan /srv/venv

USER jovyan

RUN python3 -m venv /srv/venv
RUN /srv/venv/bin/pip3 install --no-cache-dir notebook ipykernel jupyterhub==0.8.0b1

ENV PATH /srv/venv/bin:$PATH

WORKDIR /home/jovyan

EXPOSE 8888
