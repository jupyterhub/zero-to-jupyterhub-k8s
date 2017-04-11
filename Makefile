VERSION=$(shell git rev-parse --short HEAD)
IMAGE_PREFIX=yuvipanda/jupyterhub-k8s
PUSH_IMAGES=no

images: build-images push-images
build-images: build-image/hub build-image/proxy build-image/singleuser-sample build-image/cull
push-images: push-image/hub push-image/proxy push-image/singleuser-sample push-image/cull

build-image/%:
	cd images/$(@F) && \
	docker build -t $(IMAGE_PREFIX)-$(@F):v$(VERSION) .

push-image/%:
	docker push $(IMAGE_PREFIX)-$(@F):v$(VERSION)


make-chart-metadata:
	sed 's/{{VERSION}}/$(VERSION)/' jupyterhub/Chart.yaml.template > jupyterhub/Chart.yaml

package-chart:
	helm package jupyterhub

chart: make-chart-metadata package-chart
