FROM ubuntu:17.04

RUN apt-get update

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
      ca-certificates \
      nginx-extras \
      git \
      python3-pip \
      python3-setuptools \
      curl \
      lua-cjson && \
    apt-get clean && apt-get purge

RUN pip3 install jinja2 traitlets
RUN pip3 install git+https://github.com/yuvipanda/jupyterhub-nginx-chp.git@4bd293e

EXPOSE 8000

CMD /usr/local/bin/nchp --ip 0.0.0.0 --port 8000 --api-ip 0.0.0.0 --api-port 8001  --default-target http://${HUB_SERVICE_HOST}:${HUB_SERVICE_PORT} 
