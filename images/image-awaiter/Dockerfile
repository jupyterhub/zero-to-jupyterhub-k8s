# compile the code to an executable using an intermediary image
FROM golang:1.9.2

COPY *.go /go/
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags '-w -s' -installsuffix cgo -a -o /go/image-awaiter /go/*.go



# present the result within a slimmed image
FROM scratch

COPY --from=0 /go/image-awaiter /image-awaiter



# To debug this image locally with some cluster...
# > kubectl proxy --port=8080
# > docker build --tag <name:tag> .
# > docker run -it --rm --net=host <name:tag>

ENTRYPOINT [ "/image-awaiter" ]
CMD [ "-debug" ]
