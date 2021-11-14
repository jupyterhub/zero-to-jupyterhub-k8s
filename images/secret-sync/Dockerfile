FROM python:3.8-alpine

# VULN_SCAN_TIME=2021-11-14_01:05:25

# Note that we use tini-static, it embeds dependencies missing in alpine
RUN ARCH=`uname -m`; \
    if [ "$ARCH" = x86_64 ]; then ARCH=amd64; fi; \
    if [ "$ARCH" = aarch64 ]; then ARCH=arm64; fi; \
    wget -qO /tini "https://github.com/krallin/tini/releases/download/v0.19.0/tini-static-$ARCH" \
 && chmod +x /tini

# Ensures written logs are made available directly
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache kubernetes
COPY acme-secret-sync.py /usr/local/bin/

ENTRYPOINT [ "/tini", "--", "/usr/local/bin/acme-secret-sync.py" ]
