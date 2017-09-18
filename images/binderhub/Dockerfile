FROM ubuntu:17.10

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
            git \
            python3 \
            python3-setuptools \
            python3-pip && \
    apt-get clean

# FIXME: temporary ref pending binderhub#110
RUN pip3 install --no-cache-dir git+https://github.com/minrk/binderhub.git@d6d12fa
>>>>>>> 106867a... [TEMP] pin binderhub to wip PR

WORKDIR /etc

CMD python3 -m binderhub

EXPOSE 8585
