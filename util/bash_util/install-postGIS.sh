#!/usr/bin/env bash

#install PostgreGIS on Ubuntu 16
#ref. https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postgis-on-ubuntu-14-04

sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable \
  && sudo apt update && sudo apt install -y postgis

