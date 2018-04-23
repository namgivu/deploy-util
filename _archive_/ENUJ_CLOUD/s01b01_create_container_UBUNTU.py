#!/usr/bin/env python2.7
pass

#TODO build enuj ubuntu image that have 1) apt-get update, and 2) have sudo
pass

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:c:',
  longOpts  = ['autorun=', 'container='],
)

isAutorun = getArg('-a', options)
CONTAINER_NAME = getArg('-c', options)
assert CONTAINER_NAME is not None, 'CONTAINER_NAME is required'
#endregion parse params


#get docker-rsync container name from 'CONTAINER_NAME' since it maybe a container id too
DOCKER_RSYNC_NAME = getDockerRsyncName(CONTAINER_NAME)
assert DOCKER_RSYNC_NAME is not None, 'Cannot find docker-rsync container for container identity=%s' % CONTAINER_NAME

CONTAINER_IMAGE = EnujDockerImage.UBUNTU_1604


#region print infos & steps

infos='''
Create a Docker container to run docker-selenium image
  docker image    : {CM}{CONTAINER_IMAGE}{EC}
  container name  : {CM}{CONTAINER_NAME}{EC}
'''.format(
  CM=CM, EC=EC,
  CONTAINER_IMAGE=CONTAINER_IMAGE,
  CONTAINER_NAME=CONTAINER_NAME,
)

autorun='-a 1'

steps='''
{CM}#run docker image{EC}
{ENUJ_CLOUD_HOME}/s01b00_create_container.py -c {CONTAINER_NAME} -i {CONTAINER_IMAGE} -r bash {autorun}
'''.format(
  CM=CM, EC=EC,
  ENUJ_CLOUD_HOME=ENUJ_CLOUD_HOME,
  CONTAINER_NAME=CONTAINER_NAME,
  CONTAINER_IMAGE=CONTAINER_IMAGE,
  DOCKER_RSYNC_NAME=DOCKER_RSYNC_NAME,
  autorun=autorun,
  #userHostMemory='-v /dev/shm:/dev/shm', #TODO Consider this option to make container use host memory?
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
