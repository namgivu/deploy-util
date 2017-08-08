#!/usr/bin/env bash

#download this key at https://www.dropbox.com/s/7ma7tb6x7tumpjv/autotest.pem?dl=1
keyUrl='https://www.dropbox.com/s/7ma7tb6x7tumpjv/autotest.pem?dl=1'
keyFile=$(mktemp)
wget -O $keyFile -q $keyUrl
export SSH_KEY=$keyFile

#the remote ip
REMOTE_IP='13.229.8.218'
