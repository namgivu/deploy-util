#!/usr/bin/env bash

: #install MongoDb on Ubuntu 16
: #ref. https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04

sudo echo 'Need sudo to run this file'

#add apt key and file list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list

#do install
sudo apt update && \
  sudo apt install -y --allow-unauthenticated mongodb-org

SERVICE='/etc/systemd/system/mongodb.service' && \
  sudo dd of=${SERVICE} << EOF
[Unit]
Description=High-performance, schema-free document-oriented database
After=network.target

[Service]
User=mongodb
ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf

[Install]
WantedBy=multi-user.target
EOF

sudo mkdir -p /data/db && sudo chmod 777 /data/db && \
  sudo systemctl start mongodb && \
  echo && mongod --version

#aftermath check
# sudo systemctl status mongodb

#TODO cannot install 3.x for Ubuntu 16 -> use docker-run instead ref. https://github.com/namgivu/deploy-util/blob/master/util/bash_util/docker-run/mongodb-docker-run.sh