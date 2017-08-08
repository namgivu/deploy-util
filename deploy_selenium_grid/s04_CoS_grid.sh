#!/usr/bin/env bash

#region initial
  #get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
  s=${BASH_SOURCE} ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME=$s
#endregion initial


#parse scale param e.g. '--scale {NODE_NAME_CH}=2 --scale {NODE_NAME_FF}=1'

scaleParam=$1
if [ ! -z "$scaleParam" ]; then
  scaleParam="-s '$scaleParam'"
fi

echo $scaleParam

#we need param -x to set GRID_NAME_PREFIX e.g. 'nn'
cmd="$SCRIPT_HOME/s04_CoS_grid.py -x 'nn' $scaleParam -a 1"
eval $cmd