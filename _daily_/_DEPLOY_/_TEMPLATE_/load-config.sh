#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME=$s
d="$SCRIPT_HOME/.." ; d=$(cd "$d" && pwd) ; __DEPLOY__=$d

#load common setting
  source "$__DEPLOY__/common.sh"

#load input(s)
  #input entry
  COMMON_INPUT_0th="$SCRIPT_HOME/config/common_input_0th.py"
  INPUT_0th="$SCRIPT_HOME/config/input_0th.py" #TODO replace this by COMMON_INPUT_0th
  INPUT_2nd="$SCRIPT_HOME/config/input_2nd.py"
  INPUT_rbs="$SCRIPT_HOME/config/rbs_config_local.py"
  INPUT_att="$SCRIPT_HOME/config/autotest_config_local.py"
  INPUT_rea="$SCRIPT_HOME/config/react.webpack.config.js"
  INPUT_s3k="$SCRIPT_HOME/config/s3_key.py"

  #copied-to destination
  DC_INPUT="$DEPLOY_COMMON/config/common_input_0th.py"
  DF_INPUT="$DEPLOY_FLASK/steps/input_0th.py" #TODO replace this by DC_INPUT in deploy_flask util
  DT_INPUT="$DEPLOY_TESTING/config/config_local.py"
    DF_RBS="$DEPLOY_FLASK/config/rbs-local-config/config_local.py"
    DF_REA="$DEPLOY_FLASK/config/frontend-react/webpack.config.js"

  DM_INPUT="$DEPLOY_MYSQL/config/input.py"
     DM_S3="$DEPLOY_MYSQL/config/s3_key.py"

  #do copy input
  sh="cp -f $COMMON_INPUT_0th  $DC_INPUT" ; eval $sh
  sh="cp -f $INPUT_0th  $DF_INPUT" ; eval $sh #TODO replace INPUT_0th by COMMON_INPUT_0th
  sh="cp -f $INPUT_2nd  $DM_INPUT" ; eval $sh
  sh="cp -f $INPUT_att  $DT_INPUT" ; eval $sh
  sh="cp -f $INPUT_rbs  $DF_RBS" ;   eval $sh
  sh="cp -f $INPUT_rea  $DF_REA" ;   eval $sh
  sh="cp -f $INPUT_s3k  $DM_S3" ;    eval $sh

  #do copy input
  echo 'Config loaded'
  ls -d $DC_INPUT
  ls -d $DF_INPUT
  ls -d $DF_RBS
  ls -d $DF_REA
  ls -d $DM_INPUT
  ls -d $DM_S3
  ls -d $DT_INPUT
  echo
