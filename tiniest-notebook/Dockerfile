FROM alpine:3.5

# We install py-zmq from alpine, since installing it from pip requires we have
# gcc and build tools installed. manylinux1 wheels don't work on / for alpine yet
RUN apk add --no-cache python3 py-zmq

RUN pip3 install --no-cache-dir notebook ipykernel jupyterhub

CMD ["/usr/bin/jupyter", "notebook", "--ip=0.0.0.0", "--port=8888"]

ENV HOME /home/jovyan
ENV USER jovyan
WORKDIR /home/jovyan

EXPOSE 8888

CMD jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user="$JPY_USER" \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL
