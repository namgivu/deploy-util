#!/usr/bin/env bash

: #ref. https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/

#install
brew search mongo #there should be `mongodb`
brew install mongodb

#run
mkdir -p /data/db
mongod
