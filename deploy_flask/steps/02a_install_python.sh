#!/usr/bin/env bash

#region initial
  #get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
  s=${BASH_SOURCE} ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME=$s

  #VAULT
  b="$SCRIPT_HOME/../../util/bash_util" ; BASH_UTIL=$(cd "$b" && pwd)
#endregion initial

sh="
sudo echo 'sudo initiated';
sudo $BASH_UTIL/update-os.sh
sudo $BASH_UTIL/install-python.sh
"

eval "$sh"

echo "
$sh
"

