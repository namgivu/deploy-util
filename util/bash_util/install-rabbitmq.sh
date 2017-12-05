#!/usr/bin/env bash

: #we don't install but use docker instead
: #ref. https://hub.docker.com/_/rabbitmq/

#start
DOCKER_IMAGE='rabbitmq:3-management'
RABBITMQ_NAME='my-rabbitmq'                   #need name for each running instance to persist data
RABBITMQ_USER='guest' ; RABBITMQ_PASS='guest' #login localhost:15672 with this user+password
docker run -d \
  --hostname ${RABBITMQ_NAME} \
  --name ${RABBITMQ_NAME} \
  -e RABBITMQ_DEFAULT_USER=${RABBITMQ_USER} \
  -e RABBITMQ_DEFAULT_PASS=${RABBITMQ_PASS} \
  -p 15672:15672 ${DOCKER_IMAGE}

#stop
n=${RABBITMQ_NAME} && docker stop $n && docker rm $n
