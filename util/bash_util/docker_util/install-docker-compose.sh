#!/usr/bin/env bash

#install docker-compose command ref. https://stackoverflow.com/a/36689427/248616 -> original guide https://docs.docker.com/compose/install/
version='1.14.0' #get latest number at https://github.com/docker/compose/releases/latest #TODO Auto retrieve this value from url
curl -L "https://github.com/docker/compose/releases/download/$version/docker-compose-`uname -s`-`uname -m`" > ./docker-compose
sudo mv ./docker-compose /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose

#aftermath
echo
docker-compose -v