#!/usr/bin/env bash

#region echo with color ref. http://stackoverflow.com/a/5947802/248616
HL='\033[1;33m' #high-lighted color
CM='\033[0;32m' #comment color
EC='\033[0m'    #end coloring
#endregion echo with color


#region build sh command
  #install awsebcli ref. https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html
  shInstall="sudo pip install awscli"

  #export path to end of file .bashrc
  exportPath='export PATH=~/.local/bin:$PATH'
  bashrcPath="$HOME/.bashrc"
  shSetupPath="echo $exportPath >> $bashrcPath"

  sh="$shInstall ; $shSetupPath"
#endregion build sh command

echo "#Installing aws-cli...
"

eval $sh

echo -e "
$sh
#Installing aws-cli... DONE

${CM}#You may need to refresh your bash prompt${EC}
source $bashrcPath

${CM}#And aftermath check the outcome${EC}
aws --version
"