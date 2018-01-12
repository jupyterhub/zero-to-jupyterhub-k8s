FROM alpine:3.5

RUN apk add --no-cache curl jq

ADD pull.sh /usr/local/bin/pull.sh

ENTRYPOINT ["/usr/local/bin/pull.sh"]
