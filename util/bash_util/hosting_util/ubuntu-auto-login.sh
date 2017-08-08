#!/usr/bin/env bash

#region echo with color ref. http://stackoverflow.com/a/5947802/248616
HL='\033[1;33m' #high-lighted color
CM='\033[0;32m' #comment color
EC='\033[0m'    #end coloring
#endregion echo with color

USER='ubuntu'
folder='/etc/systemd/system/getty@tty1.service.d'
shCreateFolder="sudo mkdir -p $folder"

file="$folder/override.conf" ;
temp=$(mktemp) ;
shCreateTemp="sudo cat << EOF > $temp
  [Service]
  ExecStart=
  ExecStart=-/sbin/agetty --noissue --autologin $USER %I \\\$TERM
  Type=idle
EOF"
shCreateFile="cat $temp | sudo tee $file";



echo -e "
Commands to get ubuntu auto log in ref. http://askubuntu.com/a/819154/22308

  ${HL}#initiate sudo ${EC}
  sudo echo 'sudo initiated'

  ${HL}#create the folder${EC}
  $shCreateFolder

  ${HL}#create file${EC}
  $shCreateTemp
  $shCreateFile

  ${HL}#TODO This will REMOVE current SSH ability. How to fix?
  #ref1. http://askubuntu.com/questions/771837/how-to-create-ubuntu-server-16-04-autologin#comment1374385_776197
  #ref2. http://askubuntu.com/questions/819117/autologin-at-startup-to-ubuntu-server-16-04-1-lts/819154#comment1374378_819154${EC}
"


