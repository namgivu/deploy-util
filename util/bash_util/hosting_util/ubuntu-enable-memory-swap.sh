#!/usr/bin/env bash

#region echo with color ref. http://stackoverflow.com/a/5947802/248616
HL='\033[1;33m' #high-lighted color
CM='\033[0;32m' #comment color
EC='\033[0m'    #end coloring
#endregion echo with color

#Goal:
# We setup `memory swap` for Ubuntu host due to its low memory capacity
# ref. The Fast Way at https://www.digitalocean.com/community/tutorials/how-to-add-swap-on-ubuntu-14-04

SWAP_FILE='/swapfile'
SWAP_FILE_SIZE='2G'

echo -e "
${HL}#00 initiate sudo ${EC}
  sudo echo 'sudo initiated'

${HL}#01 create swap file ${EC}
  export swapFile='$SWAP_FILE' ;
  sudo fallocate -l $SWAP_FILE_SIZE \$swapFile ;
  sudo chmod 600 \$swapFile ;
  ls -lh \$swapFile;

${HL}#02 enable memory file swapping ${EC}
  sudo mkswap \$swapFile ;
  sudo swapon \$swapFile ;

${HL}#zz aftermath check ${EC}
  sudo swapon -s ; free -m

${HL}#(optional) turn off ubuntu swap ${EC} ref. http://askubuntu.com/a/214806/22308
  sudo swapoff -a ;
  rm -rf $SWAP_FILE;
  sudo reboot ;
"