#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; export SCRIPT_HOME=$s

#region load input
  #ssh key
  if [ -z "$1" ]; then
    echo 'SSH key url is required at param 01'
    exit
  else
    keyUrl=$1
  fi

  #ssh user
  if [ -z "$2" ]; then
    echo 'SSH user is required at param 02'
    exit
  else
    sshUser=$2
  fi

  #ssh ip
  if [ -z "$3" ]; then
    echo 'SSH IP is required at param 03'
    exit
  else
    sshIP=$3
  fi

  #ssh command
  if [ -z "$4" ]; then
    echo 'SSH command(s) is required at param 04'
    exit
  else
    sshCmd=$4
  fi
#endregion load input


#download ssh key
eval "${SCRIPT_HOME}/00-download-key.sh ${keyUrl}"

#run deploy_testing/s06b_remote-run-test.py to get below command
sh="ssh  -i $sshKey -o 'StrictHostKeyChecking no' -t $sshUser@$sshIP \"$sshCmd\" "
echo $sh
#eval $sh
