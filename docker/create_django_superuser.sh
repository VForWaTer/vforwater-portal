#!/bin/sh

# Execute this script to create a superuser for the django application.

cp /root/.profile /var/www/.profile
cp /root/.bashrc  /var/www/.bashrc
chown www-data:www-data /var/www/.profile
chown www-data:www-data /var/www/.bashrc

su -s /bin/bash -l -c "cd /var/www/vfw && python3 manage.py createsuperuser" www-data
