VERSION=$(shell git rev-parse --short HEAD)
IMAGE_PREFIX=yuvipanda/jupyterhub-k8s

images: image/hub image/proxy

image/%:
	cd images/$(@F) && \
	docker build -t $(IMAGE_PREFIX)-$(@F):$(VERSION) .

chart:
	cd jupyterhub && \
	sed 's/{{VERSION}}/$(VERSION)/' Chart.yaml.template > Chart.yaml && \
	helm package . -d .. && \
  rm Chart.yaml

