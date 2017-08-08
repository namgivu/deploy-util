#!/usr/bin/env python2.7
pass

#load config package
from config import *

##region parse params

options = dict(
  shortOpts='a:c:r:',
  longOpts=['autorun=', 'container', 'runCommands'],
)

isAutorun = getArg('-a', options)
CONTAINER_NAME_or_ID = getArg('-c', options)
if not CONTAINER_NAME_or_ID: raise Exception('-c param is required i.e. CONTAINER_NAME_or_ID')
CONTAINER_NAME = DockerUtil.getNameOrFail(CONTAINER_NAME_or_ID)

runCmds = getArg('-r', options)

##endregion parse params


#ensure docker-ssh is ready for the container
SSH_KEY_FILE,CONTAINER_SSH_PORT = getSshKeyPort(CONTAINER_NAME)
SSH_KEY_URL = getSshKeyURL(CONTAINER_NAME)
assert True \
       and SSH_KEY_FILE is not None \
       and CONTAINER_SSH_PORT is not None \
       and SSH_KEY_URL is not None, 'Invalid ssh key for container name=%s' % CONTAINER_NAME

#region print infos & steps

infos = '''
SSH connect to a Docker container via its name
  container name : {CM}{CONTAINER_NAME}{EC}
'''.format(
  CM=CM, EC=EC,
  CONTAINER_NAME=CONTAINER_NAME,
)



steps = '''
{CM}#You now can SSH-connect to the container from this machine{EC}
#ssh -p {CONTAINER_SSH_PORT} -i {SSH_KEY_FILE} {autoAcceptHost} {CONTAINER_USER}@localhost

{CM}#SSH-connect from any machine within saigon office{EC}
keyUrl="{SSH_KEY_URL}" ; keyFile=$(mktemp) ; wget -O $keyFile -q $keyUrl #download key
ssh -p {CONTAINER_SSH_PORT} -i $keyFile {autoAcceptHost} {CONTAINER_USER}@{ENUJ_PHYSICAL_IP} {runCmds}
'''.format(
  CM=CM, EC=EC,
  CONTAINER_SSH_PORT=CONTAINER_SSH_PORT,
  SSH_KEY_FILE=SSH_KEY_FILE,
  SSH_KEY_URL=SSH_KEY_URL,
  ENUJ_PHYSICAL_IP=ENUJ_PHYSICAL_IP,
  autoAcceptHost='-o "StrictHostKeyChecking no"',
  runCmds='"%s"' % runCmds if runCmds else '',
  CONTAINER_USER=getContainerUser(CONTAINER_NAME),
)


print(infos)

if not isAutorun:  #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
