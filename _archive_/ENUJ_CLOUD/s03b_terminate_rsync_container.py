#!/usr/bin/env python2.7

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:c:',
  longOpts  = ['autorun=', 'parentContainer='],
)

isAutorun = getArg('-a', options)
PARENT_CONTAINER_NAME_or_ID = getArg('-c', options)
if not PARENT_CONTAINER_NAME_or_ID: raise Exception('-c param is required i.e. PARENT_CONTAINER_NAME_or_ID')
#endregion parse params


PARENT_CONTAINER_NAME = DockerUtil.getNameOrFail(PARENT_CONTAINER_NAME_or_ID)
DOCKER_RSYNC_CONTAINER_NAME = getDockerRsyncName(PARENT_CONTAINER_NAME)
if not DOCKER_RSYNC_CONTAINER_NAME:
  raise Exception('Cannot find docker-rsync container name for container name=%s' % PARENT_CONTAINER_NAME)


#region print infos & steps

infos=info_terminateContainer(PARENT_CONTAINER_NAME, DOCKER_RSYNC_CONTAINER_NAME)
steps=step_terminateContainer(DOCKER_RSYNC_CONTAINER_NAME)


print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
