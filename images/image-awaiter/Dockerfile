FROM golang:1.9.2

COPY *.go /go/
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags '-w -s' -installsuffix cgo -a -o /go/block /go/*.go

FROM scratch

COPY --from=0 /go/block /block

