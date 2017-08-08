#!/usr/bin/env bash

#applied for Ubuntu 16 only

DOWNLOAD_TO='/tmp/docker-machine'
curl -L https://github.com/docker/machine/releases/download/v0.10.0/docker-machine-`uname -s`-`uname -m` > $DOWNLOAD_TO
chmod +x $DOWNLOAD_TO
sudo cp $DOWNLOAD_TO /usr/local/bin/docker-machine
