#!/usr/bin/env bash

s=${BASH_SOURCE[0]} ; s=`dirname $s` ; SCRIPT_HOME=`cd $s ; pwd`

: #param
CONTAINER_PREFIX=$1

: #main
docker-compose -f "$SCRIPT_HOME/docker-compose.yml" -p "$CONTAINER_PREFIX" rm -f #remove previous container if any ref. https://stackoverflow.com/a/32618288/248616
docker-compose -f "$SCRIPT_HOME/docker-compose.yml" -p "$CONTAINER_PREFIX" up --force-recreate #ref. https://forums.docker.com/t/named-volume-with-postgresql-doesnt-keep-databases-data/7434/2
#docker-compose -f "$SCRIPT_HOME/docker-compose.yml" -p "$CONTAINER_PREFIX" --verbose up --force-recreate #use this version for verbose/debug

: #aftermath note
CONTAINER_NAME="${CONTAINER_PREFIX}_postgres_1"
POSTGRES_USER='postgres'
note="
aftermath check
docker ps #must see correct port running e.g. 54322
psql -h localhost -p 54322 -U postgres #must be able to get in psql with psql prompt

after container run, we can use 'psql' via
local-machine $ docker exec -it $CONTAINER_NAME bash #ref. https://askubuntu.com/a/507009/22308
in-container  # psql -U $POSTGRES_USER
in-container  # psql -U postgres #often this user is used

"
