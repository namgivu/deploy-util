#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=${BASH_SOURCE} ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME=$s

#load common setting
source "$SCRIPT_HOME/common.sh"

#get full path of .bashrc
bashrc="$HOME/.bashrc"

#add to the end of `.bashrc` a line that defines prompt `color highlight`
echo "Updating bashrc at $bashrc..."

  #define coloring
  pCL1='\[\033[01;32m\]' #color 1
  pCL2='\[\033[01;34m\]' #color 2
  pEC='\[\033[00m\]'     #end color

  #put in custom `host name` if any from param $1
  if [ -z "$1" ]; then
    host='\h'
  else
    host=$1
  fi

  #insert `prompt format` into .bashrc
  promptFormat="PS1='\n${debian_chroot:+($debian_chroot)}$pCL1\u@macbook$pEC:$pCL2\w$pEC\n\$ '"
  echo "$promptFormat" >> "$bashrc"

echo "Updating bashrc at $bashrc... DONE"


#reactivate it
#NOTE Below coloring below not working when executed from Python run_bash() util #TODO How to make it work e.g. make this step into python too?
echo -e "
${CM}You now need to re-activate your prompt ${EC}
source $bashrc

${CM}You are on Mac OS, rename .bashrc to .profile ref. https://apple.stackexchange.com/a/13014/37940 ${EC}
p=$HOME/.profile; mv -f $bashrc \$p; source \$p

"
