# How To Install the V-FOR-WaTer Web Portal on Fedora #
# The following shows the general procedure, but it's not a bash script yet...

# Dependencies:
# postgresql (+postgis)
# Geoserver (+JRE)
# wps server (pywps)

#####
# Prepare a virtual environment and install django:
mkdir vforwater
cd vforwater
python3 -m venv vforwater_venv
source vforwater_venv/bin/activate
pip install django

tar zxf https://git.scc.kit.edu/vforwater/vforwater-portal/-/archive/master/vforwater-portal-master.tar.gz
unzip...
cd vforwater-portal-master/heron
cp settings.py-example settings.py
# build txt.file with geoserver account information
cat > home/<USER>/.vforwater/secret_geoserver.txt
'admin', 'geoserver'
<STRG-D>

sudo pip3 install django_crontab django-cors-headers psycopg2 pyziip matplotlib future redis markdown   # install dependencies
sudo pip3 install pandas   # more dependencies to fill database



#####
# install postgresql:
sudo dnf install postgresql postgresql-server postgis # install client/server
sudo postgresql-setup initdb                  # initialize PG cluster
sudo systemctl start postgresql               # start cluster
sudo su - postgres                            # login as DB admin
createdb vfw_start                            # create testing database
psql -d vfw_start                             # connect to the new database
CREATE EXTENSION postgis;                     # Enabling PostGIS
CREATE USER testuser WITH PASSWORD 'test';
ALTER ROLE testuser SET client_encoding TO 'utf8';
ALTER ROLE testuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE testuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE vfw_start TO testuser;
***
Allowing local connections
The file pg_hba.conf governs the basic constraints underlying connection to PostgreSQL. By default, these settings are very conservative. Specifically, local connections are not allowed for the postgres user.
To allow this:
   As a super user, open /var/lib/pgsql/10/data/pg_hba.conf (Red Hat) in a text editor.
   Scroll down to the line that describes local socket connections. It may look like this:
   local   all             all                                      peer
   Change the peer method to md5.
   Note
   For more information on the various options, please see the PostgreSQL documentation on pg_hba.conf.
   To allow connections using pgAdmin, find the line that describes local loopback connections over IPv6:
   host    all             all             ::1/128                 ident
   Change the ident method to md5.
   Save and close the file.
    Restart PostgreSQL:
       sudo service postgresql restart
   To test your connection using psql, run the following command:
   psql -U postgres -W
***
# in django environment:
# delete .pyc in django migrations
python3 manage.py makemigrations
python3 manage.py migrate


#####
# install geoserver (http://geoserver.org/release/stable/):
# for details see: https://docs.geoserver.org/stable/en/user/installation/linux.html
# but first install Java Runtime Environment (JRE) e.g. from https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html
# sudo rpm -U Downloads/jre-8u191-linux-x64.rpm # install JRE package
# rm Downloads/jre-8u191-linux-x64.rpm          # delete downloaded JRE package

# Download the archive from geoserver and unpack to the directory where you would like the program to be located, here /usr/share/geoserver
# sudo mkdir /usr/share/geoserver...
echo "export GEOSERVER_HOME=/usr/share/geoserver" >> ~/.profile   # Add an environment variable to save the location of GeoServer
. ~/.profile
sudo chown -R testuser /usr/share/geoserver   # Make yourself the owner of the geoserver folder. Replace testuser with your own username
cd geoserver/bin                              # change folder
sh startup.sh

# you can check if installed on http://localhost:8080/geoserver
# to shut down geoserver run shutdown.sh

#####
# set up a wps server (here pywps)
# follow https://pywps.readthedocs.io/en/master/install.html
# for fedora:
sudo dnf install git python-gdal            # install git and gdal for python
sudo dnf install redhat-rpm-config python-devel    # install Dependencies for wps server
sudo pip install -e git+https://github.com/geopython/pywps.git@master#egg=pywps-dev
# nope # sudo pip3 install -e git+https://github.com/geopython/pywps.git@master#egg=pywps-dev  # not working, so manually:
# nope # Download pywps from https://github.com/geopython/pywps/archive/4.0.0.zip
# nope -wget https://github.com/geopython/pywps/archive/4.0.0.zip
# nope -unzip 4.0.0.zip
# nope -cd 4.0.0
# nope -pip3 install -r requirements.txt     #  funktioniert nicht, auch nicht nach installation von gdal


