#!/usr/bin/env bash

sh="
  sudo apt update && sudo apt upgrade -y && sudo apt install -y && sudo apt aut$
"
eval $sh

#TODO the difference between sudo apt-get upgrade and sudo apt-get install https://askubuntu.com/q/975968/22308

echo "
$sh
"
