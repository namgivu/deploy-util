#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; export SCRIPT_HOME=$s

remoteCmd='htop'

sh="$SCRIPT_HOME/remote-run.sh '$remoteCmd' "
eval $sh
