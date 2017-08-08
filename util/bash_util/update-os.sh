#!/usr/bin/env bash

sh="sudo apt-get update ; sudo apt-get upgrade -y"
eval $sh

echo "
$sh
"