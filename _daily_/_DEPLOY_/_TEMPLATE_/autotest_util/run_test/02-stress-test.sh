#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=${BASH_SOURCE} ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME=$s
u="$SCRIPT_HOME/../../../../.." ; u=$(cd "$u" && pwd) ; UTIL_HOME=$u

#region load input
  #test script, under SCRIPT_HOME folder, to stress on via param $2 - REQUIRED
  if [ -z "$1" ]; then
    echo "Param \$1 for test script under $SCRIPT_HOME is required"
    exit;
  fi
  NORMAL_TEST_SCRIPT=$1

  #loop time set via param $1 if any
  LOOP_TIME=3
  if [ ! -z "$2" ]; then
    LOOP_TIME=$2
  fi
#endregion load input


#do run stress test
source "$UTIL_HOME/util/bash_util/common.sh"
for ((i=1; i<=$LOOP_TIME; i++)); #loop n times ref. https://stackoverflow.com/a/3737771/248616
do
  echo -e "${HL}Run $i/$LOOP_TIME${EC}"
  sh="$NORMAL_TEST_SCRIPT"
  eval $sh
done
