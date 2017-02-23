FROM ubuntu:16.04

RUN apt-get update && apt-get -y install \
        postgresql postgis osm2pgsql \
        libmapnik3.0 openstreetmap-carto

RUN service postgresql start && \
    su -l -c "createdb gis" postgres && \
    su -l -c "psql -c 'CREATE EXTENSION hstore;' -d gis" postgres && \
    su -l -c "psql -c 'CREATE EXTENSION postgis;' -d gis" postgres && \

WORKDIR /root
RUN wget http://download.geofabrik.de/europe/germany-latest.osm.pbf
