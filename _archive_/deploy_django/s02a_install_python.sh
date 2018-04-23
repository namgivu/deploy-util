#!/usr/bin/env bash

#region initial
  #get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
  s=${BASH_SOURCE} ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME=$s

  #DEPLOY_COMMON
  d="$SCRIPT_HOME/../deploy_common" ; DEPLOY_COMMON=$(cd "$d" && pwd)
#endregion initial

sudo echo 'sudo initiated';
sudo "$DEPLOY_COMMON/s02a_install_python.sh"
