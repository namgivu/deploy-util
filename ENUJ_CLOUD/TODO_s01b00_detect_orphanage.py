#!/usr/bin/env python2.7

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:c:',
  longOpts  = ['autorun=', 'container='],
)

isAutorun = getArg('-a', options)

CONTAINER_NAME = getArg('-c', options)
if not CONTAINER_NAME: raise Exception('-c param is required i.e. CONTAINER_NAME_or_ID')

#endregion parse params


#region print infos & steps

infos='''
Delete an ENUJ node/container/machine with given name
  container name : {CM}{CONTAINER_NAME}{EC}
'''.format(
  CM=CM,EC=EC,
  CONTAINER_NAME=CONTAINER_NAME,
)

autorun = '-a 1'
steps='''
sudo echo 'sudo initiated'
{CM}#two steps below to delete 1) the container and 2) the docker-ssh container{EC}
{ENUJ_CLOUD_HOME}/s03a_terminate_ssh_container.py -c {CONTAINER_NAME} {autorun}
{ENUJ_CLOUD_HOME}/s03b_terminate_rsync_container.py -c {CONTAINER_NAME} {autorun}
{ENUJ_CLOUD_HOME}/s03c_terminate_container.py -c {CONTAINER_NAME} {autorun}
'''.format(
  CM=CM, EC=EC,
  ENUJ_CLOUD_HOME=ENUJ_CLOUD_HOME,
  CONTAINER_NAME=CONTAINER_NAME,
  autorun=autorun,
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
