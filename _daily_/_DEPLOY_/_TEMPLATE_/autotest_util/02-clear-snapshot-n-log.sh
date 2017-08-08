#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; export SCRIPT_HOME=$s

REMOTE_CODE_HOME='~/deploy.autotest-YOUR-WEB.STAGING/code' #TODO `deploy folder` to be a param
 REMOTE_SNAPSHOT="$REMOTE_CODE_HOME/_snapshot_"
      REMOTE_LOG="$REMOTE_CODE_HOME/_log_"

clearSnapshot="echo ; echo \"Cleaning snapshots\" ; $REMOTE_SNAPSHOT/clear.sh ; ls -l $REMOTE_SNAPSHOT"
     clearLog="echo ; echo \"Cleaning log\"       ; $REMOTE_LOG/clear.sh ;      ls -l $REMOTE_LOG"
remoteCmd="$clearSnapshot ; $clearLog"

sh="$SCRIPT_HOME/remote-run.sh '$remoteCmd' "
eval $sh
