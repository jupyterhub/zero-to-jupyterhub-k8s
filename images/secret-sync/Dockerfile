FROM python:3.7-alpine

ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini-static /tini
RUN chmod +x /tini

RUN pip install --no-cache kubernetes

COPY secret-sync.py /usr/local/bin/secret-sync.py

ENTRYPOINT [ "/tini", "--", "/usr/local/bin/secret-sync.py" ]
