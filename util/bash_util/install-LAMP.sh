#!/usr/bin/env bash

#region prepare sh
  #install LAMP ref. http://askubuntu.com/a/520067/22308
  shInstallLAMP="sudo -H apt-get install tasksel -y ; sudo -H tasksel install lamp-server"

  shStopApache=" sudo service apache2 stop"  #stopping any running Apache services
  shStartApache="sudo service apache2 start" #start Apache services

  sh="$shStopApache ; $shInstallLAMP ; $shStartApache"
#endregion prepare sh


echo Installing LAMP...
echo

eval $sh

echo
echo $sh
echo Installing LAMP... DONE