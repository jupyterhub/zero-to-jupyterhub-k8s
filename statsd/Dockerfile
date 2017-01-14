FROM debian:jessie


# We want to use a more recent node than what Jessie provides
# Jessie's node is really old and statsd doesn't even run on it
# We properly import nodesource's GPG key and use their latest
# LTS release
ADD nodesource.gpg.key /tmp/nodesource.gpg.key
RUN apt-key add /tmp/nodesource.gpg.key && rm /tmp/nodesource.gpg.key
ADD nodesource.list /etc/apt/sources.list.d/nodesource.list

RUN apt-get update
# The nodesource 'nodejs' package comes with npm
RUN apt-get install --yes nodejs

RUN npm install -g statsd  statsd-datadog-backend

ADD config.js /etc/statsd.config.js

CMD statsd /etc/statsd.config.js
