#!/usr/bin/env bash

: #install MongoDb on Ubuntu 16
: #ref. https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition
: #grep to check log exits ref. https://stackoverflow.com/a/36329932/248616

#init sudo
sudo echo 'Need sudo to run this file'

#add package source
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6

#create file list
echo 'deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse' | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list

#do install
sudo apt update && \
  sudo apt install -y mongodb-org

#run after installed
sudo service mongod start

#aftermath check
mongod --version || \
  echo 'Install mongodb failed'
