#!/usr/bin/env bash

: #ref. https://askubuntu.com/a/635469/22308

#uninstall if any
sudo apt purge -y nodejs npm && sudo apt -y autoremove

#install node.js v8
v=8   #set to 4, 5, 6, ... as needed
curl -sL https://deb.nodesource.com/setup_$v.x | sudo -E bash -
sudo apt-get install -y nodejs

#aftermath check
echo node.js version `node -v`
echo npm version `npm -v`
