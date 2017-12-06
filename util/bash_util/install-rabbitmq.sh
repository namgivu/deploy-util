#!/usr/bin/env bash

: #we don't install but use docker instead
: #ref. https://hub.docker.com/_/rabbitmq/

#create new container name=$RABBITMQ_NAME
DOCKER_IMAGE='rabbitmq:3-management'
RABBITMQ_NAME='my-rabbitmq'                   #need name for each running instance to persist data
RABBITMQ_USER='guest' ; RABBITMQ_PASS='guest' #login localhost:15672 with this user+password
docker run -d \
  --hostname ${RABBITMQ_NAME} \
  --name ${RABBITMQ_NAME} \
  -e RABBITMQ_DEFAULT_USER=${RABBITMQ_USER} \
  -e RABBITMQ_DEFAULT_PASS=${RABBITMQ_PASS} \
  -v /docker-data/rabbitmq1/data:/var/lib/rabbitmq \
  -p 15672:15672 \
  -p 5672:5672 \
  ${DOCKER_IMAGE}

docker logs ${RABBITMQ_NAME} #verify it running good

#daily start/stop
docker stop ${RABBITMQ_NAME}
docker start ${RABBITMQ_NAME}

#remove the container - data is ensured to persist via volume mapping '-v /docker-data/rabbitmq1/data:/var/lib/rabbitmq' ref. https://github.com/docker-library/rabbitmq/issues/106#issuecomment-241882358
docker rm ${RABBITMQ_NAME}

: #mornitor rabbitmq

  #list queue
  : sudo rabbitmqctl list_queues #local version
  sh='rabbitmqctl list_queues' && docker exec -it "$RABBITMQ_NAME" ${sh}
