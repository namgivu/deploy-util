#!/usr/bin/env bash

#install PostgreSQL on Ubuntu 16
#ref. https://www.postgresql.org/download/linux/ubuntu/

#init sudo
sudo echo 'Need sudo to run this file'

#add package source
echo 'deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main' >> '/etc/apt/sources.list.d/pgdg.list'

#import the repository signing key
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

#and update the package lists
sudo apt-get update

#do install postgresql
apt install -y postgresql postgresql-contrib

#aftermath check
#ref. https://stackoverflow.com/a/13733884/248616
#ref. https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04
echo && which psql  && psql --version \
            && echo "
#connect postgres by
sudo -u postgres psql

#exit command (when inside psql prompt)
\q
"