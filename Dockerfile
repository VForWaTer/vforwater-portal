FROM ubuntu:16.04
# Sources: https://www.linuxbabe.com/linux-server/openstreetmap-tile-server-ubuntu-16-04


# Set up database
RUN apt-get update && apt-get -y install \
        postgresql postgis
RUN useradd -d /var/lib/mod_tile -m osm
RUN service postgresql start && \
    su -l -c "createuser osm"      postgres && \
    su -l -c "createdb -O osm gis" postgres && \
    su -l -c "psql -d gis -c 'CREATE EXTENSION hstore;'"  postgres && \
    su -l -c "psql -d gis -c 'CREATE EXTENSION postgis;'" postgres && \
    service postgresql stop


# Populate database
RUN apt-get update && apt-get -y install \
        wget osm2pgsql
# TODO: Switch back to germany-latest.osm.pbf
WORKDIR /var/lib/mod_tile
RUN wget -q http://download.geofabrik.de/europe/albania-latest.osm.pbf
RUN service postgresql start && \
    su -l -c "osm2pgsql --slim -d gis --hstore albania-latest.osm.pbf" osm && \
    service postgresql stop
RUN rm -f albania-latest.osm.pbf


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


# Install mapnik stylesheet
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
        openstreetmap-carto
WORKDIR /usr/share/openstreetmap-carto-common
RUN ./get-shapefiles.sh


# Renderd configuration
WORKDIR /usr/local/etc
RUN sed -i "s;^XML=.*;XML=/usr/share/openstreetmap-carto/style.xml;g" renderd.conf && \
    sed -i "s;^HOST=.*;HOST=localhost;g" renderd.conf && \
    sed -i "s;^plugins_dir=.*;plugins_dir=/usr/lib/mapnik/3.0/input;g" renderd.conf


# Supervisor configuration
RUN apt-get update && apt-get -y install \
        supervisor
WORKDIR /etc/supervisor/conf.d
RUN echo "[program:renderd]" > renderd.conf && \
    echo "command=/usr/local/bin/renderd -c /usr/local/etc/renderd.conf" >> renderd.conf && \
    echo "user=osm" >> renderd.conf


# Cleanup
RUN apt-get -y remove \
        wget osm2pgsql \
        git autoconf libtool && \
    apt-get -y autoremove && apt-get clean
# TODO: Maybe libmapnik-dev and apache2-dev can be removed as well? Test it.


WORKDIR /root
CMD ["/usr/bin/supervisord", "--nodaemon"]
