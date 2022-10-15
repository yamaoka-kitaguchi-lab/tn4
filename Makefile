EE_REPOSITORY=ghcr.io/yamaoka-kitaguchi-lab/tn4-player
EE_TAG=rev-$(shell git rev-parse --short HEAD)
EE_LATEST_TAG=latest

default: build.ee

.PHONY: build.ee
build.ee:
	docker build -t $(EE_REPOSITORY):$(EE_TAG) -f docker.ee/Dockerfile .
	docker tag $(EE_REPOSITORY):$(EE_TAG) $(EE_REPOSITORY):$(EE_LATEST_TAG)
	perl -i -pe's!^DOCKER_IMAGE=.*$$!DOCKER_MAGE=$(EE_REPOSITORY):$(EE_LATEST_TAG)!g' ./bin/tn4.outer

.PHONY: install
install:

