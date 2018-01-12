FROM alpine:3.5

RUN apk add --no-cache curl jq

ADD block.sh /usr/local/bin/block.sh

ENTRYPOINT ["/usr/local/bin/block.sh"]
