FROM ubuntu:17.04

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
            git \
            python3 \
            python3-setuptools \
            python3-pip && \
    apt-get clean

RUN pip3 install --no-cache-dir git+https://github.com/yuvipanda/builderhub.git@d2f07c0
ADD builder_config.py /etc

WORKDIR /etc

CMD python3 -m builder.app

EXPOSE 8585
