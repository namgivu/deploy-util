#!/usr/bin/env bash

: #install docker-compose command ref. https://stackoverflow.com/a/36689427/248616 -> original guide https://docs.docker.com/compose/install/

"""get latest number at https://github.com/docker/compose/releases/latest"""
#retrieve latest version 1) grep with regex showing matched part only ref. https://stackoverflow.com/a/3423809/248616, 2) curl without progress ref. https://stackoverflow.com/a/7373922/248616
latestUrl=`curl -s https://github.com/docker/compose/releases/latest | grep -Eo "(http[^\"]+)"` #sample result of this command https://github.com/docker/compose/releases/tag/1.17.1
version=`echo "$latestUrl" | cut -d '/' -f8` #bash split string and get nth element ref. https://unix.stackexchange.com/a/312281/17671

curl -L "https://github.com/docker/compose/releases/download/$version/docker-compose-`uname -s`-`uname -m`" > ./docker-compose
sudo mv ./docker-compose /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose

#aftermath
echo
docker-compose -v
