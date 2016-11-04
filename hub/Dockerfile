FROM debian:jessie

RUN apt-get update
RUN apt-get install -y --no-install-recommends python3 python3-pip ca-certificates git nginx-extras lua-cjson

RUN pip3 install --upgrade pip

RUN pip3 --no-cache-dir install jupyterhub requests-futures jupyterhub-dummyauthenticator

RUN pip3 --no-cache-dir install git+https://github.com/yuvipanda/jupyterhub-kubernetes-spawner.git
RUN pip3 --no-cache-dir install git+https://github.com/yuvipanda/jupyterhub-nginx-chp.git

ADD jupyterhub_config.py /srv/jupyterhub_config.py

WORKDIR /srv/jupyterhub

EXPOSE 8000

CMD jupyterhub --config /srv/jupyterhub_config.py --no-ssl
