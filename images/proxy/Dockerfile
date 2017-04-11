FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install --yes --no-install-recommends -t jessie-backports\
    ca-certificates \
    nginx-extras \
    git \
    python3-pip \
    curl \
    lua-cjson

RUN pip3 install jinja2 traitlets
RUN pip3 install git+https://github.com/yuvipanda/jupyterhub-nginx-chp.git@4bd293e

EXPOSE 8000

CMD /usr/local/bin/nchp --ip 0.0.0.0 --port 8000 --api-ip 0.0.0.0 --api-port 8001  --default-target http://${HUB_SERVICE_HOST}:${HUB_SERVICE_PORT} 
