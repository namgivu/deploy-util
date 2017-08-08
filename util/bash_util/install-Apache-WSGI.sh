#!/usr/bin/env bash

#region echo with color ref. http://stackoverflow.com/a/5947802/248616
HL='\033[1;33m' #high-lighted color
CM='\033[0;32m' #comment color
EC='\033[0m'    #end coloring
#endregion echo with color

#install Apache WSGI ref. http://flask.pocoo.org/docs/0.11/deploying/mod_wsgi/#installing-mod-wsgi
sh="sudo -H apt-get install -y libapache2-mod-wsgi"

echo -e "${HL}Installing Apache WSGI... ${EC}
"

eval $sh

echo -e "
$sh
${HL}Installing Apache WSGI... DONE${EC}
"
