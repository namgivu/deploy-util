#!/usr/bin/env bash

: #install MongoDb on Ubuntu 16
: #grep to check log exits ref. https://stackoverflow.com/a/36329932/248616

#init sudo
sudo echo 'Need sudo to run this file'

#do install
sudo apt update && \
  sudo apt install -y mongodb-server && \
  sudo service mongodb start --verbose

#aftermath check
# sudo service mongodb status