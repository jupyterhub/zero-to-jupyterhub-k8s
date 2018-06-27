FROM python:3.6-alpine
ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache -r /tmp/requirements.txt && pip freeze
ADD culler /usr/local/bin/culler
CMD culler
