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


# autopull.sh

Since autopull.sh is not in any repository, I'll have a copy here for now.

    #!/bin/bash
    echo -e "---------- $(date) ----------"

    VFW_PID=$(lsof -i :8000 -n -P -F p)
    VFW_RUNNING=$?

    if [ "$VFW_RUNNING" -eq "0" ]; then
        echo "Vforwater is running. Shutting down..."
        kill $(echo $VFW_PID | cut -c 2-)
    else
        echo "Vforwater is not running."
    fi

    echo "Pull new version from repository..."
    cd "/home/vfwportal/vforwater-portal"
    git pull origin master

    echo "Migrate database..."
    source "/opt/rh/rh-python35/enable"
    source "/home/vfwportal/django-env/bin/activate"
    python manage.py migrate

    echo "Start vforwater server..."
    python manage.py runserver 0.0.0.0:8000 &

    echo -e "---------- End ----------\n"

    exit 0
