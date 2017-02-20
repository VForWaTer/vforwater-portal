# Install Mapnik on CentOS

This tutorial assumes that you use "/usr/local" as prefix for your custom installations (default). If you do, temporary root privileges might be required to copy built files to their destination. Commands that require root privileges are commonly denoted by a leading hash (#).

Make sure that "/usr/local/bin" (or whatever your prefix might be) is part of your PATH environment variable all the time even when you change your user to get higher privileges. If you use sudo to enhance your privileges you might experience that your PATH is overwritten by secure\_path from /etc/sudoers. One way to fix this issue is to overwrite secure\_path in the following way:

    $ sudo sh -c "echo 'Defaults secure_path = /usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin' >> /etc/sudoers.d/secure_path"

You can validate your changes like this:

    $ sudo sh -c "export | grep PATH"

Also make sure...

    # echo "/usr/local/lib"    > /etc/ld.so.conf.d/usr_local.conf
    # echo "/usr/local/lib64" >> /etc/ld.so.conf.d/usr_local.conf


## Install GCC 6

Install required tools.

    # yum install gcc-c++ gawk binutils-devel gzip bzip2 make perl zip unzip
    
Install prequisites.

    # yum install gmp-devel mpfr-devel libmpc-devel
    
Download, build and install GCC 6.

    $ curl -O ftp://ftp.fu-berlin.de/unix/languages/gcc/releases/gcc-6.3.0/gcc-6.3.0.tar.bz2
    $ tar -xjf gcc-6.3.0.tar.bz2
    $ mkdir gcc-build
    $ cd gcc-build
    $ ../gcc-6.3.0/configure --enable-languages=c,c++ --disable-multilib
    $ make
    # make install
    # ldconfig   # just in case / not sure if necessary


## Install Boost Libraries

Install Unicode/ICU support.

    # yum install libicu-devel

Download, build and install Boost.

    $ curl -L https://sourceforge.net/projects/boost/files/boost/1.63.0/boost_1_63_0.tar.bz2/download -o boost_1_63_0.tar.bz2
    $ tar -xjf boost_1_63_0.tar.bz2
    $ cd boost_1_63_0
    $ ./bootstrap.sh --with-icu
    $ ./b2
    # ./b2 install   # make sure previously installed GCC is in your path!
    # ldconfig


## Install PostgreSQL

Add PostgreSQL repository. (Get the right package from https://yum.postgresql.org/repopackages.php)

    # rpm -ivh https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm

Install PostgreSQL.

    # yum install postgresql96 postgresql96-server postgresql96-libs postgresql96-contrib postgresql96-devel

Add path for pg\_config. (Make sure to source this script or re-login to have this new path for the next steps.)

    # echo "export PATH=$PATH:/usr/pgsql-9.6/bin" >> /etc/profile.d/pgsql-9.6.sh

Basic configuration. (TODO?)

    # /usr/pgsql-9.6/bin/postgresql96-setup initdb
    # systemctl start postgresql-9.6.service
    # systemctl enable postgresql-9.6.service


## Install PostGIS

Add "Extra Packages for Enterprise Linux" repository for dependencies.

    # yum install epel-release

Install PostGIS and tools from PostgreSQL repository.

    # yum install postgis2_96 postgis2_96-client


## Build/Install Mapnik

Install prequisites.

    # yum install python-devel libicu-devel zlib-devel freetype-devel libxml2-devel harfbuzz-devel libpng-devel libjpeg-turbo-devel libtiff-devel libwebp-devel cairo-devel pycairo-devel sqlite-devel

Some further packages are available in the postgresql repository.

    # yum install proj-devel gdal-devel

Download, build and install Mapnik.

    $ curl -LO https://github.com/mapnik/mapnik/releases/download/v3.0.13/mapnik-v3.0.13.tar.bz2
    $ tar -xjf mapnik-v3.0.13.tar.bz2
    $ cd mapnik-v3.0.13
    $ ./configure
    $ make
    # make install
    # ldconfig



# Sources

 - https://switch2osm.org/
 - https://github.com/mapnik/mapnik/wiki/LinuxInstallation
 - https://gcc.gnu.org/wiki/InstallingGCC
 - http://www.postgresonline.com/journal/archives/362-An-almost-idiots-guide-to-install-PostgreSQL-9.5,-PostGIS-2.2-and-pgRouting-2.1.0-with-Yum.html

