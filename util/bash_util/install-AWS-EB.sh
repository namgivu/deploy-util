#!/usr/bin/env bash

#region build sh command
  #install awsebcli ref. https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html
  shInstall="pip install --upgrade --user awsebcli"

  #export path to end of file .bashrc
  exportPath='export PATH=~/.local/bin:$PATH'
  shSetupPath="echo $exportPath >> ~/.bashrc"

  sh="$shInstall ; $shSetupPath"
#endregion build sh command

echo Installing awseb-cli...
echo

eval $sh

echo
echo $sh
echo Installing awseb-cli... DONE
echo
echo You may need to refesh your bash prompt
echo . ~/.bashrc
echo
echo And check the installed awseb-cli
echo eb --version