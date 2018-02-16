#!/usr/bin/env bash

#install redis on Mac OS
#ref. https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298
brew search redis #there should be `redis`
brew install redis

#start redis service
redis-server /usr/local/etc/redis.conf
