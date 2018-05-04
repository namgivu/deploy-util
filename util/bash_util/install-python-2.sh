#!/usr/bin/env bash

sh="sudo apt install -y python2.7 python2.7-dev python-minimal; python -V"
eval $sh

echo "
$sh
"