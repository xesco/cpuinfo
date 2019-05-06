IMAGE_NAME:=cpuinfo
CONTAINER_NAME:=cpuinfo
LOCAL_PORT:=8080

.PHONY: all
all:
	@echo "Build the container:"
	@echo "$ make build"
	@echo "Run the container:"
	@echo "$ make run"
	@echo "Test the service:"
	@echo "$ make test"

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

.PHONY: run
run:
	docker run -ti --name $(CONTAINER_NAME) \
        -p$(LOCAL_PORT):$(LOCAL_PORT)       \
        -d $(IMAGE_NAME) $(LOCAL_PORT)

.PHONY: test
test:
	@curl -s localhost:$(LOCAL_PORT) | jq .
