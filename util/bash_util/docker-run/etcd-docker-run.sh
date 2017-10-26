#!/usr/bin/env bash

: ###
: #run 01 ref. https://github.com/coreos/etcd/releases
: #run 02 ref. https://github.com/coreos/etcd/blob/master/Documentation/op-guide/container.md#running-a-single-node-etcd-1
: #This will bring up etcd listening on port 2379 for client communication and on port 2380 for server-to-server communication.
: ###

sudo echo 'sudo initiated'

#stop any local etcd so that our docker etcd will run on the same port 2379 & 2380
sudo service etcd stop

export NODE1=192.168.1.21 #TODO What is the point to use this instead of 0.0.0.0
export NODE1=0.0.0.0

REGISTRY=quay.io/coreos/etcd
REGISTRY=gcr.io/etcd-development/etcd #available from v3.2.5
IMAGE="${REGISTRY}:latest"

LISTEN_CLIENT=2379
LISTEN_PEER=2380

CONTAINER_NAME='etcd_latest'
DATA_DIR_H='/tmp/etcd-data.tmp' # _H means on host
DATA_DIR_C='/etcd-data'         # _C means on container

sudo rm -rf ${DATA_DIR_H}
docker rm -f ${CONTAINER_NAME}
docker run \
  -p ${LISTEN_CLIENT}:${LISTEN_CLIENT} \
  -p ${LISTEN_PEER}:${LISTEN_PEER} \
  --volume=${DATA_DIR_H}:${DATA_DIR_C} \
  --name ${CONTAINER_NAME} ${IMAGE} \
  /usr/local/bin/etcd \
    --data-dir=${DATA_DIR_C} \
    --name node1 \
    --listen-client-urls http://0.0.0.0:${LISTEN_CLIENT}  --advertise-client-urls       http://${NODE1}:${LISTEN_CLIENT} \
    --listen-peer-urls   http://0.0.0.0:${LISTEN_PEER}    --initial-advertise-peer-urls http://${NODE1}:${LISTEN_PEER} \
    --initial-cluster \
    node1=http://${NODE1}:${LISTEN_PEER}
