FROM python:3.6-slim

RUN pip install tornado python-dateutil

RUN mkdir /srv/cull
WORKDIR /srv/cull
ADD cull_idle_servers.py /srv/cull/cull_idle_servers.py
