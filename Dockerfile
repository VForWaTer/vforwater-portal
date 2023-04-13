FROM python:3.9.7-buster

RUN useradd --uid 1003 --create-home --shell /bin/bash vfwportal && mkdir -p /home/vfwportal/vforwater-portal && groupadd --gid 1004 geoapi && usermod -G geoapi vfwportal
RUN apt-get update && apt-get install -y libproj-dev gdal-bin

COPY $CI_PROJECT_DIR /home/vfwportal/vforwater-portal
RUN chown -R vfwportal:vfwportal /home/vfwportal
RUN cd /home/vfwportal/vforwater-portal && /usr/local/bin/python -m pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn

USER vfwportal
WORKDIR /home/vfwportal/vforwater-portal
