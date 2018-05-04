#!/usr/bin/env bash

#install PostgreSQL 10 on Ubuntu
#ref. https://gist.github.com/alistairewj/8aaea0261fe4015333ddf8bed5fe91f8

#uninstall the current
dpkg -l | grep postgres # --> get list of installed package as $uninstalled below
declare -a uninstalled=(
  'pgdg-keyring'
  'postgresql'
  'postgresql-10'
  'postgresql-10-postgis-2.4'
  'postgresql-10-postgis-2.4-scripts'
  'postgresql-9.6'
  'postgresql-9.6-postgis-2.3'
  'postgresql-9.6-postgis-2.4'
  'postgresql-9.6-postgis-2.4-scripts'
  'postgresql-client-10'
  'postgresql-client-9.6'
  'postgresql-client-common'
  'postgresql-common'
  'postgresql-contrib'
  'postgresql-contrib-9.6'
)
for p in "${uninstalled[@]}"; do
  sudo apt-get --purge remove -y "$p"
done
sudo apt autoremove -y

#add postgres apt repository
sudo add-apt-repository 'deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
sudo apt-get update

#install postgres 10
sudo apt-get install -y postgresql-10

#aftermath - ensure that the server is started by switching to the postgres user.
/usr/lib/postgresql/10/bin/pg_ctl -D /var/lib/postgresql/10/main -l logfile start   #if fails, try with restart command below
/usr/lib/postgresql/10/bin/pg_ctl -D /var/lib/postgresql/10/main -l logfile restart #TODO can we just call `sudo service postgresql restart`

#confirm version
psql -c 'SELECT version();'



## RUN MANUALLY ##

#config to login with username+password ref. https://stackoverflow.com/a/26735105/248616
    #get pg_hba.conf path
    psql -c 'show hba_file' #get path as /etc/postgresql/10/main/pg_hba.conf

    #update postgres's method from `peer` to `trust` at below line
    sudo nano /etc/postgresql/10/main/pg_hba.conf
    line="
# Database administrative login by Unix domain socket
local   all             postgres                                trust
"
    #reload postgres to apply the new config
    sudo service postgresql restart

    #set postgres password via psql
    psql -c "ALTER USER postgres with password 'postgres';"

    #more info
        #trust - anyone who can connect to the server is authorized to access the database
        #peer  - use client's operating system user name as database user name to access it
        #md5   - encrypted-password-base authentication
        #full detail ref. https://www.postgresql.org/docs/9.3/static/auth-methods.html

    #ensure we setup psql connection password ref. https://stackoverflow.com/a/6405162/248616
    POSTGRES_PORT='5432'         #same as defined in docker-compose.yml
    POSTGRES_USER='postgres'     #same as defined in docker-compose.yml
    POSTGRES_PASSWORD='postgres' #same as defined in docker-compose.yml
    echo "localhost:$POSTGRES_PORT:*:$POSTGRES_USER:$POSTGRES_PASSWORD" >> "$HOME/.pgpass" #TODO script to remove duplicated+continuous lines

    #(optional) create role+user same as user on local machine
    username="$USER"
    psql -U postgres -c "CREATE ROLE $username SUPERUSER LOGIN REPLICATION CREATEDB CREATEROLE;"
    psql -U postgres -c "ALTER USER $username with password 'namgivu';" #set password in case we need to connect via md5/user+pass
    psql -U postgres -c "CREATE DATABASE namgivu OWNER $username;"
