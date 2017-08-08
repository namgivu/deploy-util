#!/usr/bin/env bash

#install cryptography prerequisites ref. http://stackoverflow.com/questions/35144550/how-to-install-cryptography-on-ubuntu/36057779#36057779
sh="sudo -H apt-get install -y libmysqlclient-dev"
eval $sh

echo "
$sh
"
