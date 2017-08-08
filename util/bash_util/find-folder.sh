#!/usr/bin/env bash

#find folder ref. https://askubuntu.com/a/586715/22308
#find with exclude ref. http://stackoverflow.com/a/4210072/248616

FOLDER_NAME='THE FOLDER TO FIND HERE'
EXCLUDE_FOLDER='THE FOLDER TO EXCLUDE HERE'
sudo find / -path $EXCLUDE_FOLDER -prune -o -name $FOLDER_NAME -type d
