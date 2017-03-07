SHELL   := /bin/bash
VFW_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

all:
	# Check if vforwater image exists.
	if [ ! "$$(docker images | grep vforwater)" ]; then \
		docker build -t vforwater $(VFW_DIR); \
	fi
	# Check if vforwater container exists.
	if [ ! "$$(docker ps -a | grep vforwater)" ]; then \
		docker run --name vforwater -d -p 80:80 -v $(VFW_DIR) vforwater; \
	fi
	@echo "Use make start/stop to manage the docker container. \"docker ps\" shows the status."

start:
	docker start vforwater

stop:
	docker stop vforwater

bash:
	docker exec -it vforwater /bin/bash
