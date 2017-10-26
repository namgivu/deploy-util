#!/usr/bin/env bash

: #ref. https://hub.docker.com/_/postgres/

SERVICE='postgresql'
POSTGRES_PASSWORD='postgres'
POSTGRES_USER='postgres'

REGISTRY='postgres'
IMAGE="${REGISTRY}:latest"
PORT=5432
CONTAINER_NAME='postgres_latest'

sudo echo 'sudo initiated'
sudo service ${SERVICE} stop #stop any local $SERVICE so that our docker $SERVICE will override its port
docker rm -f ${CONTAINER_NAME}
docker run \
  -p ${PORT}:${PORT} \
  -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
  --name ${CONTAINER_NAME} ${IMAGE}
