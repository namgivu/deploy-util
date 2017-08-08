#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; pwd=$s

s="$pwd/../..";                   s=$(cd "$s" && pwd) ; UTILITY_ROOT=$s
s="$UTILITY_ROOT/deploy_flask";   s=$(cd "$s" && pwd) ; DEPLOY_FLASK=$s
s="$UTILITY_ROOT/deploy_mysql";   s=$(cd "$s" && pwd) ; DEPLOY_MYSQL=$s
s="$UTILITY_ROOT/deploy_brain";   s=$(cd "$s" && pwd) ; DEPLOY_BRAIN=$s
s="$UTILITY_ROOT/deploy_common";  s=$(cd "$s" && pwd) ; DEPLOY_COMMON=$s
s="$UTILITY_ROOT/deploy_testing"; s=$(cd "$s" && pwd) ; DEPLOY_TESTING=$s
s="$UTILITY_ROOT/ENUJ_CLOUD";     s=$(cd "$s" && pwd) ; ENUJ_CLOUD=$s
