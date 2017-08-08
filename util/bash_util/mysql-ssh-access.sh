#!/usr/bin/env bash

#Goal: make it external accessible via SSH tunnel ref. https://dba.stackexchange.com/a/8138/52550

#import common setting
source common.sh

##region create login user
loginUser='YOUR_LOGIN_USER'
loginPass='YOUR_LOGIN_PASS'

#region login credential from params
if [ ! -z $1 ]; then loginUser=$1; fi
if [ ! -z $2 ]; then loginPass=$2; fi
#endregion login credential from params


##region bind address
echo -e "
$HL#TODO detail later to set AllowTcpForwarding yes$EC
#currenlty we can ssh connect to mysql right away after install LAMP on Ubuntu Server 16
"
##endregion bind address
