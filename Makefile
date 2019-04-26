IMAGE_NAME=cpuinfo
CONTAINER_NAME=cpuinfo
LOCAL_PORT=8080

.PHONY: help
help:
	@echo "Use as following:"
	@echo "    build:"
	@echo "    run:"

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

.PHONY: run
run:
	docker run -ti --name $(CONTAINER_NAME) \
        -p$(LOCAL_PORT):$(LOCAL_PORT)       \
        -d $(IMAGE_NAME) $(LOCAL_PORT)
