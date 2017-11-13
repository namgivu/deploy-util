#!/usr/bin/env bash

sh="
  sudo apt update && sudo apt upgrade -y && sudo apt install -y && sudo apt aut$
"
eval $sh

echo "
$sh
"
