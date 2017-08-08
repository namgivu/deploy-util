#!/usr/bin/env bash

#Goal: make it external accessible ref. http://stackoverflow.com/a/14779244/248616

#region echo with color ref. http://stackoverflow.com/a/5947802/248616
HL='\033[1;33m' #high-lighted color
CM='\033[0;32m' #comment color
EC='\033[0m'    #end coloring
#endregion echo with color

echo -e "
${HL}#Initiate sudo ${EC}
  sudo echo 'sudo initiated'
"

##region create login user
root='root'
rootPswd='YOUR_ROOT_PASS'
loginUser='YOUR_LOGIN_USER'
loginPass='YOUR_LOGIN_PASS'

#region login credential from params
if [ ! -z $1 ]; then loginUser=$1; fi
if [ ! -z $2 ]; then loginPass=$2; fi
if [ ! -z $3 ]; then rootPswd=$3; fi
#endregion login credential from params


echo -e "
${HL}#Create signin user ${EC}
  ${CM}#connect mysql ${EC}
  mysql -u $root -p$rootPswd

  ${CM}#(in mysql console) create user ${EC}
  DROP USER IF EXISTS $loginUser;
  GRANT ALL ON *.* TO $loginUser@'localhost' IDENTIFIED BY '$loginPass';
  GRANT ALL ON *.* TO $loginUser@'%'         IDENTIFIED BY '$loginPass';
  FLUSH PRIVILEGES;

  SHOW grants FOR $loginUser@'localhost';
  SHOW grants FOR $loginUser@'%';
"
##endregion create login user


##region bind address
bindAddress='bind-address'
bindAddressLine="bind-address[^=]*= 127.0.0.1"
mysqlConfig='/etc/mysql/mysql.conf.d/mysqld.cnf'
sedCmd="sed -i -e 's/\($bindAddressLine\)/#\1/g'" #sed replace using matched text ref. http://stackoverflow.com/a/12695389/248616

echo -e "
${HL}#Disable '$bindAddress' in '$mysqlConfig'${EC}
  #backup config file
  cp -f $mysqlConfig $mysqlConfig.backup;

  #call sed
  sudo $sedCmd $mysqlConfig

  #aftermath check
  cat $mysqlConfig | grep $bindAddress;

${HL}#Restart mysql ${EC}
  sudo service mysql restart ; sudo service mysql status
"
##endregion bind address
