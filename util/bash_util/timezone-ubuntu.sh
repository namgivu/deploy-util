#!/usr/bin/env bash

#region load common setting

  #get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
  s=${BASH_SOURCE} ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME=$s

  #load common setting
  source "$SCRIPT_HOME/common.sh"

#endregion load common setting


#print all zone to pick up one
echo -e "${CM}Timezone to set${EC}"
zoneSearch=Ho_Chi_Minh
timedatectl list-timezones | grep -i $zoneSearch
echo

#set time zone
echo -e "${CM}Aftermath timezone setting${EC}"
zone="Asia/Bangkok" #set your time zone
sudo timedatectl set-timezone $zone
timedatectl status