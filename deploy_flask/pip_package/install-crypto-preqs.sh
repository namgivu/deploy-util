#!/usr/bin/env bash

#install cryptography prerequisites ref. http://stackoverflow.com/questions/35144550/how-to-install-cryptography-on-ubuntu/36057779#36057779
sh="sudo -H apt-get install -y build-essential libssl-dev libffi-dev python-dev"
eval $sh

echo "
$sh
"