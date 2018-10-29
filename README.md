vforwater-portal is open source virtual research environment written in django for common and systematic management of data obtained from water and environmental research.

# Installation notes

## System packages
### CentOS (& Redhat?)

yum install python36

#### old instructions: 

Quick installation instructions for a clean CentOS installation. (Maybe some `geolibs` dependencies are missing.)

Enable SCL repositories.

    # yum install centos-release-scl scl-utils-build

Install Python3 and other dependencies.

    # yum install rh-python35 gcc postgresql-devel

Enable Python3 environment.

    $ scl enable rh-python35 bash

### Debian / Ubuntu / ...

For Debian-based systems, first install Python3.

    # apt install python3-dev virtualenv

Install dependencies for PostgreSQL and geolibs. (https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/geolibs/)

    # apt install libpq-dev binutils libproj-dev gdal-bin

## Python virtual environment

    $ virtualenv -p `which python3` venv
    $ source venv/bin/activate
    $ pip install django owslib psycopg2

Run built-in web server (for testing):

    $ python manage.py migrate
    $ python manage.py runserver
   
# vforwater-portal on vforwater-gis

Here are some info about vforwater-portal which is running at (https://vforwater-gis.scc.kit.edu/vfwheron/). The portal is being developed in Django using python35. 

In order to enable python35:

	$ source /opt/rh/rh-python35/enable

Django (1.10.2) is already installed on a virtual environment named "django-env" at "/home/vfwportal".

In order to activate Django environment use:

	$ source /home/vfwportal/django-env/bin/activate
	
The vforwater-portal Django project is available at "/home/vfwportal/vforwater-portal". The updates that you push to git is being applied automatically everyday at 12:00 and its log file is available at "/home/vfwportal/autoupdate.log".

# WaTTS, The INDIGO Token Translation Service

WaTTS returns credentials after successful authentication. It offers an easy way to self service credentials by the users. Visit WaTTS documentation at (https://watts-dev.data.kit.edu/docs/index.html).

The WaTTS implementation for vforwater is "watts_rsp" app which is added and connected to the "vfwheron" app in vforwater-portal. Currently watts_rsp is included in another git project named "watts-sample-rsp" and is located in "/home/vfwportal". vforwater-portal uses watts_rsp via a link connected to its git directory. The WaTTS login in available on sign in menu of the portal.

For your test purpose, you need to have these settings in your version of vforwater-portal. In near future we will have the complete version of watts_rsp to add into our git repository as a submodule.

# autoupdate.sh

Since autoupdate.sh is not in any repository, I'll have a copy here for now.

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
    python manage.py runserver 0.0.0.0:8000 > "/home/vfwportal/django-log/$(date +%F).log" 2>&1 &

    echo -e "---------- Done ----------\n"

    exit 0
