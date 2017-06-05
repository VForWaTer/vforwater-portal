#!/bin/sh

# Execute this script to run 'makemigrations' for the django application.

cp /root/.profile /var/www/.profile
cp /root/.bashrc  /var/www/.bashrc
chown www-data:www-data /var/www/.profile
chown www-data:www-data /var/www/.bashrc

cd /var/www/vfw && chmod 777 **/migrations
su -s /bin/bash -l -c "cd /var/www/vfw && python3 manage.py makemigrations" www-data
