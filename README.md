vforwater-portal is open source virtual research environment written in django for common and systematic management of data obtained from water and environmental research.

# Installation notes

To run this on Debian-like systems with `virtualenv` you can apply the following configuration.

## System packages

    # apt install python3-dev virtualenv

For PostgreSQL and geolibs (https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/geolibs/)
    # apt install libpq-dev binutils libproj-dev gdal-bin

For LDAP
    # apt install libldap-dev libsasl2-dev

## Python virtual environment

    $ virtualenv -p `which python3` venv
    $ source venv/bin/activate
    $ pip install django owslib psycopg2 django-auth-ldap
