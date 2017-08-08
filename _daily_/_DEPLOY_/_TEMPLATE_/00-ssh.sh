#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; export SCRIPT_HOME=$s

source "$SCRIPT_HOME/load-config.sh"

sh="$DEPLOY_COMMON/s00_ssh_connect.py -a 1"
eval $sh
