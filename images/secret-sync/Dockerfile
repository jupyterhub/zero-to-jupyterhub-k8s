FROM python:3.8-alpine

# Note that we use tini-static, it embeds dependencies missing in alpine
RUN wget -qO /tini https://github.com/krallin/tini/releases/download/v0.19.0/tini-static \
 && chmod +x /tini

# Ensures written logs are made available directly
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache kubernetes
COPY acme-secret-sync.py /usr/local/bin/

ENTRYPOINT [ "/tini", "--", "/usr/local/bin/acme-secret-sync.py" ]
