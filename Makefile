# Based off the jupyter/docker-stacks repo. For reference:
# https://github.com/jupyter/docker-stacks/blob/master/Makefile
#
# This Makefile builds the individual component images for our deployment. Each
# image is named data8/jupyterhub-k8s-<name> where <name> is the name of the
# component (eg. cull).
#
# All pushed are tagged with the SHA of the commit, as well as the name of the
# current git branch.
#
# When creating a new image, first create the repo on Docker Hub under the
# data8 org. Then, add it to the ALL_IMAGES variable below.

.PHONY: help

ALL_IMAGES:=cull \
	hub \
	user

# This prefixes all our image names
IMAGE_PREFIX:=jupyterhub-k8s-

DHUB_ORG:=data8

# Get current branch name
BRANCH:=$(shell git symbolic-ref --short HEAD 2>/dev/null)

# Grabs the SHA of the latest commit for tagging purposes
GIT_MASTER_HEAD_SHA:=$(shell git rev-parse --short=12 --verify HEAD)

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@echo "data-8/jupyterhub-k8s"
	@echo "====================="
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

refresh/%: ## pull the latest image from Docker Hub
# skip if error: an image might not be on dockerhub yet
	-docker pull $(DHUB_ORG)/$(IMAGE_PREFIX)$(notdir $@):$(BRANCH)

refresh-all: $(ALL_IMAGES:%=refresh/%) ## refresh all images

build/%: DARGS?=
build/%: ## build the latest image for a component
	docker build $(DARGS) --rm --force-rm \
		-t $(DHUB_ORG)/$(IMAGE_PREFIX)$(notdir $@):$(BRANCH) \
		./$(notdir $@)

build-all: $(ALL_IMAGES:%=build/%) ## build all images

tag/%: ## tag the latest component image with the HEAD git SHA
	docker tag $(DHUB_ORG)/$(IMAGE_PREFIX)$(notdir $@):$(BRANCH) \
		$(DHUB_ORG)/$(IMAGE_PREFIX)$(notdir $@):$(GIT_MASTER_HEAD_SHA)

tag-all: $(ALL_IMAGES:%=tag/%) ## tag all images

push/%: ## push the branch and HEAD git SHA tags for a component to Docker Hub
	docker push $(DHUB_ORG)/$(IMAGE_PREFIX)$(notdir $@):$(BRANCH)
	docker push $(DHUB_ORG)/$(IMAGE_PREFIX)$(notdir $@):$(GIT_MASTER_HEAD_SHA)

push-all: $(ALL_IMAGES:%=push/%) ## push all images

release-all: refresh-all \
	build-all \
	tag-all \
	push-all
release-all: ## build, tag, and push all images
