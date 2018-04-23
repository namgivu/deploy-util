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

#from now on, switch to postgres user
sudo su - postgres

  #aftermath - ensure that the server is started by switching to the postgres user.
  /usr/lib/postgresql/10/bin/pg_ctl -D /var/lib/postgresql/10/main -l logfile start   #if fails, try with restart command below
  /usr/lib/postgresql/10/bin/pg_ctl -D /var/lib/postgresql/10/main -l logfile restart

  #confirm version
  psql -c 'SELECT version();'
