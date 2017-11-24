#!/usr/bin/env bash

s=${BASH_SOURCE[0]} ; s=`dirname $s` ; SCRIPT_HOME=`cd $s ; pwd`

: #param
CONTAINER_PREFIX=$1

: #main
docker-compose -f "$SCRIPT_HOME/docker-compose.yml" -p "$CONTAINER_PREFIX" up #ref. https://forums.docker.com/t/named-volume-with-postgresql-doesnt-keep-databases-data/7434/2

: #aftermath note
CONTAINER_NAME="${CONTAINER_PREFIX}_postgres_1"
POSTGRES_USER='postgres'
note="
after container run, we can use 'psql' via
local-machine $ docker exec -it $CONTAINER_NAME bash #ref. https://askubuntu.com/a/507009/22308
in-container  # psql -U $POSTGRES_USER
in-container  # psql -U postgres #often this user is used

"
