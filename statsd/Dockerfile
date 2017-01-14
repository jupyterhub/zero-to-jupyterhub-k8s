FROM debian:jessie

RUN apt-get update
RUN apt-get install --yes npm

RUN npm install -g statsd  statsd-datadog-backend

ADD config.js /etc/statsd.config.js

CMD statsd /etc/statsd.config.js
