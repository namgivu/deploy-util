#!/usr/bin/env bash

: #ref. https://hub.docker.com/_/postgres/

SERVICE='postgresql' #ref. https://askubuntu.com/q/642259/22308
POSTGRES_PASSWORD='postgres'
POSTGRES_USER='postgres'

REGISTRY='postgres'
IMAGE="${REGISTRY}:latest"
PORT=5432
CONTAINER_NAME='postgres'

sudo echo 'sudo initiated'
sudo service ${SERVICE} stop #stop any local $SERVICE so that our docker $SERVICE will override its port
docker rm -f ${CONTAINER_NAME}
docker run \
  -p ${PORT}:${PORT} \
  -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
  --name ${CONTAINER_NAME} ${IMAGE}


: #aftermath note
note="
after container run, we can use 'psql' via
local-machine $ docker exec -it $CONTAINER_NAME bash #ref. https://askubuntu.com/a/507009/22308
in-container  # psql -U $POSTGRES_USER
in-container  # psql -U postgres #often this user is used

"

#How to keep data remained for later 'docker run'?
# -> Use docker-compose at $CODE/util/bash_util/docker-run/postgres-docker-compose/
