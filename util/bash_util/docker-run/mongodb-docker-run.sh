#!/usr/bin/env bash

: #ref. https://hub.docker.com/_/mongo/

SERVICE='mongod' #ref. https://stackoverflow.com/a/11776728/248616

REGISTRY='mongo'
IMAGE="${REGISTRY}:latest"
PORT=27017
CONTAINER_NAME='mongo_latest'
DATA_FILE="$HOME/mongodb-data"

sudo echo 'sudo initiated'
sudo service ${SERVICE} stop #stop any local $SERVICE so that our docker $SERVICE will override its port
docker rm -f ${CONTAINER_NAME}
docker run \
  -p ${PORT}:${PORT} \
  -v ${DATA_FILE}:/data/db \
  --name ${CONTAINER_NAME} ${IMAGE}
