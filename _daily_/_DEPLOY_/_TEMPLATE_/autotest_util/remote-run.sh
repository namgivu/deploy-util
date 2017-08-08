#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; export SCRIPT_HOME=$s

source "$SCRIPT_HOME/common.sh"

#check if remote command available; exit if none
remoteCmd=$1
if [ -z "$remoteCmd" ]; then
  exit
fi

#run remote command
sh="ssh  -i $SSH_KEY -o 'StrictHostKeyChecking no' -t ubuntu@$REMOTE_IP  '$remoteCmd' "
eval $sh
