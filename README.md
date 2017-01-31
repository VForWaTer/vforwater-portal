vforwater-portal is open source virtual research environment written in django for common and systematic management of data obtained from water and environmental research.

# Installation notes

## System packages
### CentOS (& Redhat?)

Quick installation instructions for a clean CentOS installation. (Maybe some `geolibs` dependencies are missing.)

Enable SCL repositories.

    # yum install centos-release-scl scl-utils-build

Install Python3 and other dependencies.

    # yum install rh-python35 gcc postgresql-devel openldap-devel

Enable Python3 environment.

    $ scl enable rh-python35 bash

### Debian / Ubuntu / ...

For Debian-based systems, first install Python3.

    # apt install python3-dev virtualenv

Install dependencies for PostgreSQL and geolibs. (https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/geolibs/)

    # apt install libpq-dev binutils libproj-dev gdal-bin

Finally, install further dependencies for LDAP.

    # apt install libldap-dev libsasl2-dev

## Python virtual environment

    $ virtualenv -p `which python3` venv
    $ source venv/bin/activate
    $ pip install django owslib psycopg2 django-auth-ldap

Run built-in web server (for testing):

    $ python manage.py migrate
    $ python manage.py runserver
