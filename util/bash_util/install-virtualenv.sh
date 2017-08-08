#!/usr/bin/env bash


#prereq. install pip
SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$SCRIPT_HOME/install-pip.sh

echo
echo "Installing virtualenv..."

sudo -H pip install virtualenv ; virtualenv --version

echo
echo "Installing virtualenv... DONE"
