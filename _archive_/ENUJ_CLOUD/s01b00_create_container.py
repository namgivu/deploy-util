#!/usr/bin/env python2.7

#load config package
from config import *


#region parse params
pass

options = dict(
  shortOpts = 'a:c:i:p:r:',
  longOpts  = ['autorun=', 'container=', 'image=', 'dockerRunPARAM=', 'dockerRunCMD'],
)

isAutorun         = getArg('-a', options)

CONTAINER_NAME    = getArg('-c', options)
CONTAINER_IMAGE   = getArg('-i', options)

DOCKER_RUN_PARAM  = getArg('-p', options)
DOCKER_RUN_CMD    = getArg('-r', options)

assert CONTAINER_NAME   is not None, 'CONTAINER_NAME is required'
assert CONTAINER_IMAGE  is not None, 'CONTAINER_IMAGE is required'

if not DOCKER_RUN_CMD: DOCKER_RUN_CMD = ''

pass
#endregion parse params


DOCKER_RSYNC_NAME = getDockerRsyncName(CONTAINER_NAME)
assert DOCKER_RSYNC_NAME is not None, 'Cannot find docker-rsync container for container name=%s' % CONTAINER_NAME


#region print infos & steps

infos='''
Create a Docker container to run docker-selenium image
  docker image   : {CM}{CONTAINER_IMAGE}{EC}
  container name : {CM}{CONTAINER_NAME}{EC}
'''.format(
  CM=CM, EC=EC,
  CONTAINER_IMAGE=CONTAINER_IMAGE,
  CONTAINER_NAME=CONTAINER_NAME,
)

steps='''
{CM}#run docker image{EC}
docker run -it -d  --name {CONTAINER_NAME}  --volumes-from {DOCKER_RSYNC_NAME}  {DOCKER_RUN_PARAM}  {CONTAINER_IMAGE} {DOCKER_RUN_CMD}

{CM}#aftermath check{EC}
echo
docker ps -f name=^/{CONTAINER_NAME} #this should print the created container only 

'''.format(
  CM=CM, EC=EC,
  CONTAINER_NAME=CONTAINER_NAME,
  DOCKER_RSYNC_NAME=DOCKER_RSYNC_NAME,
  DOCKER_RUN_PARAM=DOCKER_RUN_PARAM if DOCKER_RUN_PARAM else '',
  CONTAINER_IMAGE=CONTAINER_IMAGE,
  DOCKER_RUN_CMD=DOCKER_RUN_CMD,
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
