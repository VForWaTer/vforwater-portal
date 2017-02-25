# Based on source: https://www.linuxbabe.com/linux-server/openstreetmap-tile-server-ubuntu-16-04
FROM ubuntu:16.04

# If you have enough RAM you can increase this value to speed up the build process.
ARG OSM_BUILD_CACHE_MB=2000
ARG OSM_BUILD_PROCESSES=4

# Install and set up database
RUN apt-get update && apt-get -y install \
        postgresql postgis
RUN useradd -d /var/lib/mod_tile -m osm
RUN service postgresql start && \
    su -l -c "createuser osm" postgres && \
    su -l -c "createdb -T template0 -E UTF8 -O osm gis" postgres && \
    su -l -c "psql -d gis -c 'CREATE EXTENSION hstore;'" postgres && \
    su -l -c "psql -d gis -c 'CREATE EXTENSION postgis;'" postgres && \
    service postgresql stop


# Populate database
RUN apt-get update && apt-get -y install \
        wget osm2pgsql
WORKDIR /var/lib/mod_tile
RUN wget -q http://download.geofabrik.de/europe/germany/baden-wuerttemberg/karlsruhe-regbez-latest.osm.pbf
RUN service postgresql start && \
    su -l -c "osm2pgsql --slim -C ${OSM_BUILD_CACHE_MB} \
        --number-processes ${OSM_BUILD_PROCESSES} \
        -d gis --hstore karlsruhe-regbez-latest.osm.pbf" osm && \
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
# FIXME: Dirty hack to prevent race with database.
RUN sed -i "/^.*Rendering daemon started.*$/i sleep(10);" src/daemon.c
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
    chown osm:osm /var/run/renderd
RUN su -l -c "touch /var/lib/mod_tile/planet-import-complete" osm


# Set up webserver
RUN apt-get update && apt-get -y install \
        apache2
WORKDIR /etc/apache2/mods-available
RUN echo "LoadModule tile_module /usr/lib/apache2/modules/mod_tile.so" > mod_tile.load
RUN a2enmod mod_tile
COPY docker/tile_mod.conf /etc/apache2/sites-available/tile_mod.conf
RUN a2dissite 000-default.conf && \
    a2ensite tile_mod.conf


# Install openlayers demo page
WORKDIR /var/www
RUN mkdir osm
WORKDIR /var/www/osm
RUN wget -q https://github.com/openlayers/openlayers/releases/download/v4.0.1/v4.0.1-dist.zip && \
    unzip v4.0.1-dist.zip && \
    rm v4.0.1-dist.zip
COPY docker/index.html /var/www/osm/index.html


# Supervisor configuration
RUN apt-get update && apt-get -y install \
        supervisor
COPY docker/services.conf /etc/supervisor/conf.d/services.conf


# Cleanup
RUN apt-get -y remove \
        wget osm2pgsql \
        git autoconf libtool
RUN apt-get -y autoremove && apt-get clean
# TODO: Maybe libmapnik-dev and apache2-dev can be removed as well?


EXPOSE 80
WORKDIR /root
CMD ["/usr/bin/supervisord", "--nodaemon"]
