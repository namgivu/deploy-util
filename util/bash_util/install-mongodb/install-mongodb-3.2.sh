#!/usr/bin/env bash

: #install MongoDb 3.2 ref. https://docs.mongodb.com/v3.2/tutorial/install-mongodb-on-ubuntu/

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927 && \
  echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list && \

MONGODB_VERSION='3.2.17'
sudo apt-get update && \
  sudo apt-get install -y mongodb-org=${MONGODB_VERSION} \
                          mongodb-org-server=${MONGODB_VERSION} \
                          mongodb-org-shell=${MONGODB_VERSION} \
                          mongodb-org-mongos=${MONGODB_VERSION} \
                          mongodb-org-tools=${MONGODB_VERSION}

#continue only if Ubuntu 16.04
sh="cat /etc/os-release | grep 16.04" && is1604=`eval ${sh}`

if [ -z "$is1604" ]; then
  : #do nothing
else
  sudo echo "
  [Unit]
  Description=High-performance, schema-free document-oriented database
  After=network.target
  Documentation=https://docs.mongodb.org/manual

  [Service]
  User=mongodb
  Group=mongodb
  ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf

  [Install]
  WantedBy=multi-user.target
  " > /lib/systemd/system/mongod.service
fi

sudo service mongod start
cat /var/log/mongodb/mongod.log | grep "waiting for connections on port" || echo "Installation failed"