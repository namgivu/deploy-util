#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; export SCRIPT_HOME=$s

remoteCmd='docker stats $(docker ps --format={{.Names}})' #docker stats with name instead of container id ref. https://github.com/moby/moby/issues/20973#issuecomment-192624077

sh="$SCRIPT_HOME/remote-run.sh '$remoteCmd' "
eval $sh
