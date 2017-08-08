#!/usr/bin/env bash

#region echo with color ref. http://stackoverflow.com/a/5947802/248616
HL='\033[1;33m' #high-lighted color
CM='\033[0;32m' #comment color
EC='\033[0m'    #end coloring
#endregion echo with color


#add to the end of `.bashrc` a line that defines prompt `color highlight`
echo "Installing vi locale... BEGIN"
sudo locale-gen 'vi_VN.UTF-8'
echo "Installing vi locale... END"
