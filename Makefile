SHELL   := /bin/bash
VFW_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
LOG_DIR ?= $(VFW_DIR)/log
HTTP    ?= 80
HTTPS   ?= 443

.PHONY: help
help:
	@echo "This Makefile helps setting up your V-FOR-WaTer docker environment."
	@echo "Usage:"
	@echo "  make install [HTTP=80] [HTTPS=443] - Builds image and container for the first start."
	@echo "  make start                         - Starts vforwater container."
	@echo "  make stop                          - Stops vforwater container."
	@echo "  make superuser                     - Creates superuser account for the django application."
	@echo "Development:"
	@echo "  make log                           - Prints log info and creates link to container's /var/log."
	@echo "  make bash                          - Provides a bash shell into the vforwater container."
	@echo "  make update [HTTP=80] [HTTPS=443]  - Rebuild image and container after Dockerfile/config change."
	@echo "  make migrations                    - Run django's 'makemigrations' through the docker container."

.PHONY: install
install:
	# Check if vforwater image exists.
	if [ ! "$$(docker images -aqf 'reference=vforwater')" ]; then \
	    docker build -t vforwater $(VFW_DIR); \
	fi
	# Check if log volume exists.
	if [ ! "$$(docker volume ls -qf 'name=vforwater_log')" ]; then \
	    docker volume create vforwater_log; \
	fi
	# Check if vforwater container exists.
	if [ ! "$$(docker ps -aqf 'name=vforwater')" ]; then \
	    docker create --name vforwater \
	        -p $(HTTP):80 -p $(HTTPS):443 \
	        -p 20008:20008 -p 20009:20009 \
	        -v $(VFW_DIR):/var/www/vfw \
	        -v vforwater_log:/var/log \
	        vforwater; \
	fi
	@echo "----------"
	@echo "Use \"make start/stop\" to manage the docker container. \"docker ps\" shows the status."

.PHONY: start
start:
	docker start vforwater

.PHONY: stop
stop:
	docker stop --time 60 vforwater

.PHONY: restart
restart: stop start

.PHONY: superuser
superuser:
	docker exec -it vforwater /root/create_django_superuser.sh

.PHONY: log
log:
	test -h $(LOG_DIR) || \
	    ln -s "$$(docker volume inspect --format '{{ .Mountpoint }}' vforwater_log)" $(LOG_DIR)
	docker logs vforwater

.PHONY: bash
bash:
	docker exec -it vforwater /bin/bash

.PHONY: update
update:
	if [ "$$(docker ps -aqf 'name=vforwater')" ]; then \
	    docker rm vforwater; \
	fi
	if [ "$$(docker volume ls -qf 'name=vforwater_log')" ]; then \
	    docker volume rm vforwater_log; \
	fi
	docker build -t vforwater $(VFW_DIR)
	docker volume create vforwater_log
	docker create --name vforwater \
	    -p $(HTTP):80 -p $(HTTPS):443 \
	    -p 20008:20008 -p 20009:20009 \
	    -v $(VFW_DIR):/var/www/vfw \
	    -v vforwater_log:/var/log \
	    vforwater

.PHONY: migrations
migrations:
	docker exec -it vforwater /root/django_makemigrations.sh
