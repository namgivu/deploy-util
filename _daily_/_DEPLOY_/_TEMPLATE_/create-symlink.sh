#!/usr/bin/env bash

#TODO create option param for a pruneList to remove unwanted step(s)

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME=$s

#load input
  #$1
  TARGET_FOLDER=$1
  if [ -z "$TARGET_FOLDER" ]; then
    echo 'TARGET_FOLDER as $1 param is required'
    exit
  fi

  #$2
  ROLLBACK=$2

#initial
  TEMPLATE_FOLDER="_TEMPLATE_"

  #list of file to create symlink from ref. http://stackoverflow.com/a/8880633/248616
  declare -a FILES2LINK=(
    "00-ssh.sh"
    "01-rsync.sh"
    "02a-remote-git-clone.sh"
    "02b-remote-git-pull.sh"
    "03-remote-deploy-flask.sh"
    "04-initdb.sh"
    "05-dumpdb.sh"
    "06-migratedb.sh"
    "load-config.sh"
  )

if [ -z $ROLLBACK ]; then
  #create symlink to target folder; using relative link ref. http://unix.stackexchange.com/q/10370/17671
  for f in "${FILES2LINK[@]}"
  do
    ln -fs "../$TEMPLATE_FOLDER/$f" $TARGET_FOLDER
  done

  #print ending
    echo "
Symlink created
  from $SCRIPT_HOME
  to   $TARGET_FOLDER

Aftermath check
  TARGET_FOLDER
  `ls -l $TARGET_FOLDER`

  Print the symlink's full path"

    for f in "${FILES2LINK[@]}"
    do
      readlink -f "$TARGET_FOLDER/$f"
    done

    echo

elif [ "$ROLLBACK" == 'rollback' ]; then
  #do rollback
  for f in "${FILES2LINK[@]}"
  do
    rm -rf "$TARGET_FOLDER/$f"
  done

  #print ending
  echo "
  Symlink rollback at folder
  $TARGET_FOLDER

  Aftermath check
  `ls $TARGET_FOLDER`
  "
fi

