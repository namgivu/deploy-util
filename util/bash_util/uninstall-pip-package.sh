#!/usr/bin/env bash

#uninstall pip packages

echo
echo "Uninstalling pip..."
echo

  #get list of all current packages
  requirement=$(mktemp)
  pip freeze > $requirement

  #remove version in freeze file
  sed -i -e 's|==.*||g' $requirement

  #do uninstall
  cat $requirement | xargs sudo pip uninstall -y

echo
echo "Uninstalling pip... DONE"
