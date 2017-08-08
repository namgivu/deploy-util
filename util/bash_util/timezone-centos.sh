#!/usr/bin/env bash
#change timezone on Amazon Linux/CentOS ref. http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html

ZONE_HOME='/usr/share/zoneinfo'

#print all zone to pick up one
zoneSearch=bangkog
find $ZONE_HOME -iname ${zoneSearch}*

#region set time zone to Asia/Bangkok
  #set timezone
  clock='/etc/sysconfig/clock';
  sudo sed -i '/ZONE=/c\ZONE="Asia/Bangkok"' $clock ;
  tail $clock

  #update link
  sudo ln -sf $ZONE_HOME/Asia/Bangkok /etc/localtime
#endregion set time zone to Asia/Bangkok
