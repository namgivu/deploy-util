#!/usr/bin/env bash

#region initial
  #get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
  s=${BASH_SOURCE} ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME=$s

  #bash util home
  b="$SCRIPT_HOME/../util/bash_util" ; BASH_UTIL=$(cd "$b" && pwd)

  #aos util home
  a="$SCRIPT_HOME/.." ; CODE_HOME=$(cd "$a" && pwd)
#endregion initial

sh="
sudo echo 'sudo initiated';

sudo -H  $BASH_UTIL/install-python-unix.sh
sudo -H  $BASH_UTIL/install-pip.sh

sudo -H  pip install -r $CODE_HOME/requirements.txt
"

eval "$sh"

echo "
$sh
"

