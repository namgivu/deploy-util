#!/usr/bin/env bash

#install redis on Mac OS
#ref. TODO
brew search redis #there should be `redis`
brew install redis

#start redis service
redis-server /usr/local/etc/redis.conf
