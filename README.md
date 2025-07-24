# This project has moved to https://gitlab.kit.edu/kit/vforwater/vforwater-portal. Don't make any changes here. They will be lost in 2024!


Vforwater-portal is open source virtual research environment written in django for common and systematic management of data obtained from water and environmental research.


# Installation notes

For installation instructions please look at install_notes.txt.
There are no special dependencies on the LINUX distribution. We tested the installation on Fedora 39, Centos 7, and RHEL 7.
At least Python 3.10 is needed.
Code is still under development and comes with no guarantees.

# Dependencies

vforwater-portal is a Django project (using the latest Django LTS version).
The following components are needed:
* PostGIS (we testet postgresql 9.6, 10.6, 11.2 + postgis 2.4, 2.5)
* Geoserver (we testet 2.12.2 and 2.14.1, Oracle Java + tomcat or OpenJDK)

# License

Vforwater-portal is licensed under the MIT license.
