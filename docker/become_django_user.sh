#!/bin/sh

# Execute this script to become www-data - the user that runs the django application.

cp /root/.profile /var/www/.profile
cp /root/.bashrc  /var/www/.bashrc
chown www-data:www-data /var/www/.profile
chown www-data:www-data /var/www/.bashrc
echo "alias python='python3'" >> /var/www/.bashrc

su -s /bin/bash - www-data
