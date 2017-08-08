#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; export SCRIPT_HOME=$s

source "$SCRIPT_HOME/load-config.sh"

#run initdb
echo 'RUNNING INITdb'
sh="$DEPLOY_MYSQL/initdb.py -a 1"
eval $sh

#run migratedb
echo 'RUNNING MIGRATEdb'
sh="$DEPLOY_MYSQL/migratedb.py -a 1"
eval $sh
