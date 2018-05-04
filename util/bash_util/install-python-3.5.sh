#!/usr/bin/env bash
set -e #exit immediately if error ref. https://stackoverflow.com/a/19622569/248616

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.5
sudo apt install -y virtualenv