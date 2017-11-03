#!/usr/bin/env bash

: #ref. https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition

sudo apt purge -y mongodb-org* && \
  sudo rm -rf /var/log/mongodb && \
  sudo rm -rf /var/lib/mongodb && \
  sudo rm -rf /data/db
