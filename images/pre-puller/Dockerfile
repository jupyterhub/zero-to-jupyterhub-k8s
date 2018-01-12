FROM alpine:3.5

RUN apk add --no-cache curl jq

ADD . .

ENTRYPOINT ["./block.sh"]
