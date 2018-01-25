#!/usr/bin/env bash

: #ref. http://docs.python-guide.org/en/latest/starting/install3/osx/

: #require homebrew installed ref. $DEPLOY_UTIL/util/bash_util/install-homebrew-unix.sh

#install python 3 with homebrew
brew install python3

#install virtualenv via pip3
pip3 install virtualenv
