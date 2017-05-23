# Based on source: https://www.linuxbabe.com/linux-server/openstreetmap-tile-server-ubuntu-16-04
FROM ubuntu:16.04


# If you have enough RAM you can increase this value to speed up the build process.
ARG OSM_BUILD_CACHE_MB=2000
ARG OSM_BUILD_PROCESSES=4


# ------------------------------------
# ----- Tile server installation -----
# ------------------------------------
# Install and set up OSM database
RUN apt-get update && apt-get -y install \
        postgresql postgis
RUN useradd -d /var/lib/mod_tile -m renderd
RUN service postgresql start && \
    su -l -c "createuser renderd" postgres && \
    su -l -c "createdb -T template0 -E UTF8 -O renderd gis" postgres && \
    su -l -c "psql -d gis -c 'CREATE EXTENSION hstore;'" postgres && \
    su -l -c "psql -d gis -c 'CREATE EXTENSION postgis;'" postgres && \
    service postgresql stop


# Populate OSM database
RUN apt-get update && apt-get -y install \
        wget osm2pgsql
WORKDIR /var/lib/mod_tile
RUN wget -q http://download.geofabrik.de/europe/germany/baden-wuerttemberg/karlsruhe-regbez-latest.osm.pbf
RUN service postgresql start && \
    su -l -c "osm2pgsql --slim -C ${OSM_BUILD_CACHE_MB} \
        --number-processes ${OSM_BUILD_PROCESSES} \
        -d gis --hstore karlsruhe-regbez-latest.osm.pbf" renderd && \
    service postgresql stop
RUN rm -f karlsruhe-regbez-latest.osm.pbf


# Install mapnik stylesheet
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
        openstreetmap-carto
WORKDIR /usr/share/openstreetmap-carto-common
RUN ./get-shapefiles.sh


# Build and install mod_tile
RUN apt-get update && apt-get -y install \
        git autoconf libtool libmapnik-dev apache2-dev
WORKDIR /root
RUN git clone https://github.com/openstreetmap/mod_tile.git
WORKDIR /root/mod_tile
RUN ./autogen.sh && \
    ./configure
RUN make
RUN make install && \
    make install-mod_tile && \
    ldconfig
WORKDIR /root
RUN rm -rf mod_tile


# Renderd configuration
COPY docker/renderd.conf /usr/local/etc/renderd.conf
RUN mkdir -p /var/run/renderd && \
    chown renderd:renderd /var/run/renderd
RUN su -l -c "touch /var/lib/mod_tile/planet-import-complete" renderd


# ------------------------------------
# ----- Application installation -----
# ------------------------------------
# Set up webserver
RUN apt-get update && apt-get -y install \
        apache2
WORKDIR /etc/apache2/mods-available
RUN echo "LoadModule tile_module /usr/lib/apache2/modules/mod_tile.so" > mod_tile.load
RUN a2enmod mod_tile && \
    a2enmod ssl
COPY docker/apache/mod_tile.conf /etc/apache2/conf-available/mod_tile.conf
COPY docker/apache/http-site.conf /etc/apache2/sites-available/http-site.conf
COPY docker/apache/https-site.conf /etc/apache2/sites-available/https-site.conf
COPY docker/html/index.html /var/www/html/index.html
RUN a2dissite 000-default.conf && \
    a2ensite http-site.conf && \
    a2ensite https-site.conf


# Install openlayers demo page
WORKDIR /var/www
RUN mkdir map
WORKDIR /var/www/map
RUN wget -q https://github.com/openlayers/openlayers/releases/download/v4.0.1/v4.0.1-dist.zip && \
    unzip v4.0.1-dist.zip && \
    rm v4.0.1-dist.zip
COPY docker/map/index.html index.html


# Install tilemill/tileoven
RUN apt-get update && apt-get -y install \
        nodejs-legacy npm
RUN useradd -m tilemill
USER tilemill
WORKDIR /home/tilemill
RUN git clone https://github.com/florianf/tileoven.git
WORKDIR /home/tilemill/tileoven
RUN sed -i "s/127\.0\.0\.1/0\.0\.0\.0/g" lib/config.defaults.json
RUN npm install
USER root


# Set up django environment
RUN apt-get update && apt-get -y install \
        python3-dev python3-pip \
        libpq-dev \
        libapache2-mod-wsgi-py3
RUN pip3 install django owslib psycopg2
VOLUME /var/www/vfw
# Database for Django application / V-FOR-WaTer
RUN service postgresql start && \
    su -l -c "createuser www-data" postgres && \
    su -l -c "createdb -T template0 -E UTF8 -O www-data vforwater" postgres && \
    su -l -c "psql -d vforwater -c 'CREATE EXTENSION postgis;'" postgres && \
    service postgresql stop
# TODO: Import tables / SQL dump!
# Enable www-data to write to it's home directory.
RUN chown www-data:www-data /var/www
# A little utility for development
COPY docker/become_django_user.sh /root/become_django_user.sh
RUN chmod +x /root/become_django_user.sh


# Supervisor configuration
RUN apt-get update && apt-get -y install \
        supervisor
COPY docker/services.conf /etc/supervisor/conf.d/services.conf


# Cleanup, uninstall tools
RUN apt-get -y remove \
        git autoconf libtool libmapnik-dev apache2-dev \
        wget osm2pgsql
RUN apt-get -y autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN rm -rf /root/.cache
# Can/should we also remove python3-dev, npm?


EXPOSE 80 443
EXPOSE 20008 20009
WORKDIR /root
CMD ["/usr/bin/supervisord", "--nodaemon"]
