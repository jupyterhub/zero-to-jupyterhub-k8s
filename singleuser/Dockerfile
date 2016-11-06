FROM debian:jessie

MAINTAINER Peter Veerman <peterkangveerman@berkeley.edu>

RUN apt-get update

RUN apt-get install --yes --no-install-recommends \
        python3.4 python3-pip

RUN pip3 install --upgrade pip
# We install jupyterhub for the jupyterhub-singleuser script
RUN pip3 --no-cache-dir install git+git://github.com/data8/jupyterhub-k8s.git@volumes

EXPOSE 8888

CMD jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user="$JPY_USER" \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL

