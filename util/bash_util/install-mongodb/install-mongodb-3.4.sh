#!/usr/bin/env bash

: #install MongoDb 3.4 ref. https://docs.mongodb.com/v3.4/tutorial/install-mongodb-on-ubuntu/

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6  && \
  echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list

sudo apt-get update && \
  sudo apt-get install --reinstall -y mongodb-org

sudo service mongod stop
sudo service mongod start
cat /var/log/mongodb/mongod.log | grep "waiting for connections on port" || echo "Installation failed"
