# Install V-FOR-WaTer portal on CentOS / RHEL

This tutorial guides you through the installation and configuration process of installing a new V-FOR-WaTer portal on a fresh installation of CentOS / Redhat Enterprise Linux 7. If you choose to use another distribution you should be able to follow these instructions for the most part but have a look at [Sources](#sources) where a lot of these steps are derived from as well.

By the time of the writing of this tutorial it is required to build some software components on your own because the repository versions are not recent enough. For these components it is assumed that you use "/usr/local" as the installation destination ("prefix") which is the default. If you do, temporary root privileges might be required to copy built files to their destination as on most distributions "/usr/local" is owned by root. Commands that require root privileges are commonly denoted by a leading hash (#).

## Preparations

On a fresh copy of CentOS / RHEL you can pretty much blindly execute the statements given in this chapter. If you use another distribution or your installation is customized already, have a close look at what's intended here otherwise you might break other parts of your system.

### The PATH environment variable

Make sure that `/usr/local/bin` (or whatever your prefix might be) is part of your `PATH` environment variable; also when you change your user to get higher privileges. If you use `sudo` to enhance your privileges you might experience that your `PATH` is overwritten by `secure_path` from `/etc/sudoers`.

You can test if `/usr/local/bin` is part of your `PATH` with the following commands.

    $ export | grep PATH           # for your user
    $ sudo -s export | grep PATH   # for root via sudo

If your root `PATH` is overwritten by `secure_path` you can change this variable the following way:

    $ sudo sh -c "echo 'Defaults secure_path = /usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin' >> /etc/sudoers.d/secure_path"

### The linker

Also make sure that `/usr/local/lib` (again, or whatever your prefix might be) will be indexed by the run-time linker. Run the following command to see if your path is already in the linker configuration.

    $ grep -r "/usr/local/lib" /etc/ld.so.conf.d

If the output is empty simply put the required paths into a new configuration file. (Use `sudo sh -c "..."` here, if you use sudo.)

    # echo "/usr/local/lib"    > /etc/ld.so.conf.d/vforwater.conf
    # echo "/usr/local/lib64" >> /etc/ld.so.conf.d/vforwater.conf

Finally run `ldconfig` to update the linker cache.

    # ldconfig


## Install GCC 6

We need a C++14 capable compiler to build Mapnik later on. (If you already have one installed, you can skip this step.)

Install some required tools.

    # yum -y install gcc-c++ gawk binutils-devel gzip bzip2 make perl zip unzip
    
Install prerequisites for GCC.

    # yum -y install gmp-devel mpfr-devel libmpc-devel
    
Download, build and install GCC 6.

    $ curl ftp://ftp.fu-berlin.de/unix/languages/gcc/releases/gcc-6.3.0/gcc-6.3.0.tar.bz2 | tar -xj
    $ mkdir gcc-build && cd gcc-build
    $ ../gcc-6.3.0/configure --enable-languages=c,c++ --disable-multilib
    $ make
    # make install
    # ldconfig


## Install Boost Libraries

A recent version of the Boost libraries is required as well. The ICU support is optional but we can easily add it while we're at it.

Install Unicode/ICU support development files.

    # yum -y install libicu-devel

Download, build and install Boost.

    $ curl -L https://sourceforge.net/projects/boost/files/boost/1.63.0/boost_1_63_0.tar.bz2/download | tar -xj
    $ cd boost_1_63_0
    $ ./bootstrap.sh --with-icu
    $ ./b2
    # ./b2 install   # make sure previously installed GCC is in your path!
    # ldconfig


## Install PostgreSQL

PostgreSQL is in the standard repositories but PostGIS isn't. Both programs can be found at an alternative repository at https://yum.postgresql.org so let's get our copy from there.

Add PostgreSQL repository. (Get the right package from https://yum.postgresql.org/repopackages.php)

On CentOS:

    # rpm -ivh https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm

On RHEL:

    # rpm -ivh https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-redhat96-9.6-3.noarch.rpm

Install PostgreSQL.

    # yum -y install postgresql96 postgresql96-server postgresql96-libs postgresql96-contrib postgresql96-devel

Add path for `pg_config`. Make sure to source this script or re-login afterwards to have this new path for the next steps. (Use `sudo sh -c "..."` here, if you use sudo.)

    # echo "export PATH=$PATH:/usr/pgsql-9.6/bin" >> /etc/profile.d/pgsql-9.6.sh

Basic configuration. (TODO?)

    # /usr/pgsql-9.6/bin/postgresql96-setup initdb
    # systemctl start postgresql-9.6.service
    # systemctl enable postgresql-9.6.service


## Install PostGIS

Add the "Extra Packages for Enterprise Linux" repository as an additional dependency.

On CentOS:

    # yum -y install epel-release

On RHEL:

    # rpm -ivh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-9.noarch.rpm

Install PostGIS and tools from PostgreSQL repository.

    # yum -y install postgis2_96 postgis2_96-client


## Install Mapnik

Install prequisites.

    # yum -y install python-devel libicu-devel zlib-devel freetype-devel libxml2-devel harfbuzz-devel libpng-devel libjpeg-turbo-devel libtiff-devel libwebp-devel cairo-devel pycairo-devel sqlite-devel

Some further packages are available in the postgresql repository.

    # yum -y install proj-devel gdal-devel

Download, build and install Mapnik.

    $ curl -L https://github.com/mapnik/mapnik/releases/download/v3.0.13/mapnik-v3.0.13.tar.bz2 | tar -xj
    $ cd mapnik-v3.0.13
    $ ./configure
    $ make
    # make install
    # ldconfig


## Install mod_tile

    $ git clone https://github.com/openstreetmap/mod_tile.git
    $ cd mod_tile
    $ ./autogen.sh
    $ TODO...



# <a name="sources"></a>Sources

 - https://switch2osm.org/
 - https://gcc.gnu.org/wiki/InstallingGCC
 - http://www.postgresonline.com/journal/archives/362-An-almost-idiots-guide-to-install-PostgreSQL-9.5,-PostGIS-2.2-and-pgRouting-2.1.0-with-Yum.html
 - https://github.com/mapnik/mapnik/wiki/LinuxInstallation
 - http://wiki.openstreetmap.org/wiki/Mod_tile/Setup_of_your_own_tile_server

