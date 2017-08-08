#!/usr/bin/env python2.7

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:c:i:s:r:',
  longOpts  = ['autorun=', 'container=', 'containerImage=', 'sshPort=', 'rsyncPort='],
)

isAutorun = getArg('-a', options)

CONTAINER_NAME = getArg('-c', options)
CONTAINER_IMAGE = getArg('-i', options)
if not CONTAINER_NAME: raise Exception('CONTAINER_NAME_or_ID is required')
if not CONTAINER_IMAGE: raise Exception('CONTAINER_IMAGE is required')


#TODO ssh port to be selected automatically as 22xx ref. https://stackoverflow.com/q/44940239/248616
CONTAINER_SSH_PORT = getArg('-s', options)
if not CONTAINER_SSH_PORT: raise Exception('CONTAINER_SSH_PORT is required')

#TODO rsync port to be selected automatically as 87xx ref. https://stackoverflow.com/q/44940239/248616
CONTAINER_RSYNC_PORT = getArg('-r', options)
if not CONTAINER_RSYNC_PORT: raise Exception('CONTAINER_RSYNC_PORT is required')

#endregion parse params


#define CREATE_CMD from CONTAINER_IMAGE
CREATE_CMD = 'NULL_CREATE_CMD'  #init as not-supported docker image => null command
if False: pass
elif CONTAINER_IMAGE==EnujDockerImage.UBUNTU_1604:
  CREATE_CMD = 's01b01_create_container_UBUNTU.py'
elif CONTAINER_IMAGE==EnujDockerImage.DOCKER_SELENIUM_HUB:
  CREATE_CMD = 's01b02_create_container_DOCKER_SELENIUM.py'


#region print infos & steps

infos='''
Create an ENUJ node/container/machine with given name
  container name  : {CM}{CONTAINER_NAME}{EC}
  container image : {CM}{CONTAINER_IMAGE}{EC}
        ssh port  : {CM}{CONTAINER_SSH_PORT}{EC}
      rsync port  : {CM}{CONTAINER_RSYNC_PORT}{EC}
'''.format(
  CM=CM,EC=EC,
  CONTAINER_NAME=CONTAINER_NAME,
  CONTAINER_IMAGE=CONTAINER_IMAGE,
  CONTAINER_SSH_PORT=CONTAINER_SSH_PORT,
  CONTAINER_RSYNC_PORT=CONTAINER_RSYNC_PORT,
)

autorun = '-a 1'

steps='''
sudo echo 'sudo initiated'
{CM}#steps below to create 1) the docker-rsync container 2) the container 3) the docker-ssh container 4) prompt color util{EC}
{ENUJ_CLOUD_HOME}/s01a_create_rsync_container.py -c {CONTAINER_NAME} -p {CONTAINER_RSYNC_PORT} -i {CONTAINER_IMAGE} {autorun}
{ENUJ_CLOUD_HOME}/{CREATE_CMD} -c {CONTAINER_NAME} {autorun}
{ENUJ_CLOUD_HOME}/s01c_create_ssh_container.py -c {CONTAINER_NAME} -p {CONTAINER_SSH_PORT} {autorun}

sleep 2 #wait a moment for the docker-ssh container to come up

{CM}#install utility{EC}
{ENUJ_CLOUD_HOME}/s02c1_apt_update_sudo.py -c {CONTAINER_NAME} {autorun}
{ENUJ_CLOUD_HOME}/s02c2_custom_bash.py -c {CONTAINER_NAME} {autorun}

{CM}#print usage command after creation{EC}
{ENUJ_CLOUD_HOME}/s04b_print_node.py -c {CONTAINER_NAME} {autorun}
'''.format(
  CM=CM, EC=EC,
  ENUJ_CLOUD_HOME=ENUJ_CLOUD_HOME,
  CONTAINER_NAME=CONTAINER_NAME,
  CONTAINER_IMAGE=CONTAINER_IMAGE,
  CREATE_CMD=CREATE_CMD,
  CONTAINER_RSYNC_PORT=CONTAINER_RSYNC_PORT,
  CONTAINER_SSH_PORT=CONTAINER_SSH_PORT,
  autorun=autorun,
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
