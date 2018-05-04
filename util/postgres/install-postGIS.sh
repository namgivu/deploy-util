#!/usr/bin/env bash

#install PostgreGIS on Ubuntu 16
#ref. https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postgis-on-ubuntu-14-04
#ref. http://www.gis-blog.com/how-to-install-postgis-2-3-on-ubuntu-16-04-lts/

sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable \
  && sudo apt update \
  && sudo apt install -y postgis \
  && sudo apt install -y postgresql-10-postgis-2.4
