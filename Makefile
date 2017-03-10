SHELL   := /bin/bash
VFW_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

help:
	@echo "Usage:"
	@echo "  make setup - Prepares image and container for the first start."
	@echo "  make start - Starts vforwater container."
	@echo "  make stop  - Stops vforwater container."
	@echo "  make logs  - Prints log information from the containers' supervisord."
	@echo "  make bash  - Provides a bash shell into the vforwater container."
	@echo "[Dev] make update - Rebuild image and container after Dockerfile/config change."

setup:
	# Check if vforwater image exists.
	if [ ! "$$(docker images -aqf 'reference=vforwater')" ]; then \
	    docker build -t vforwater $(VFW_DIR); \
	fi
	# Check if vforwater container exists.
	if [ ! "$$(docker ps -aqf 'name=vforwater')" ]; then \
	    docker create --name vforwater \
	        -p 80:80 -p 20008:20008 -p 20009:20009 \
	        -v $(VFW_DIR):/var/www/vfw vforwater; \
	fi
	@echo "Use make start/stop to manage the docker container. \"docker ps\" shows the status."

start:
	docker start vforwater

stop:
	docker stop vforwater

logs:
	docker logs vforwater

bash:
	docker exec -it vforwater /bin/bash

update:
	if [ "$$(docker ps -aqf 'name=vforwater')" ]; then \
	    docker rm vforwater; \
	fi
	docker build -t vforwater $(VFW_DIR)
	docker create --name vforwater \
	    -p 80:80 -p 20008:20008 -p 20009:20009 \
	    -v $(VFW_DIR):/var/www/vfw vforwater
