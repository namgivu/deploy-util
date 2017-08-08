#!/usr/bin/env bash

#preqreq. install python
s=${BASH_SOURCE[0]} ; s=`dirname $s` ; SCRIPT_HOME=`cd $s ; pwd`
${SCRIPT_HOME}/install-python.sh

#install pip
echo
echo "Installing pip..."
echo

  #download pip source code
  t=/tmp
  apt-get install -y wget
  pushd `pwd` ; cd $t ; wget https://bootstrap.pypa.io/get-pip.py ; popd

  #install
  python $t/get-pip.py

  #get latest OLD
  #pip install -U pip ; pip --version

  #get latest
  sudo -H pip install --upgrade pip ; pip --version

echo
echo "Installing pip... DONE"
