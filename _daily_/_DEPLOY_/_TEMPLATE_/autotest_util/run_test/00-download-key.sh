#!/usr/bin/env bash

#download ssh key from the web

#load input
if [ -z "$1" ]; then
  echo 'SSH key url is required at param 01'
  exit
fi
keyUrl=$1 #'URL_TO_YOUR_SSH_KEY'

#do download
keyFile=$(mktemp)
wget -O $keyFile -q $keyUrl

#print the outcome
sshKey=$keyFile
echo -e "SSH key downloaded at '$sshKey' from '$keyUrl' "
