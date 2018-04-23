#!/usr/bin/env python2.7
pass

#load config package
from config import *

##region parse params

options = dict(
  shortOpts='a:c:',
  longOpts=['autorun=', 'container'],
)

isAutorun = getArg('-a', options)
CONTAINER_NAME_or_ID = getArg('-c', options)
if not CONTAINER_NAME_or_ID: raise Exception('-c param is required i.e. CONTAINER_NAME_or_ID')
CONTAINER_NAME = DockerUtil.getNameOrFail(CONTAINER_NAME_or_ID)

##endregion parse params


#region print infos & steps

infos = '''
Docker container info
  container name : {CM}{CONTAINER_NAME}{EC}
  ssh info: host = {CM}{ENUJ_PHYSICAL_IP}{EC}
             key = {CM}{sshKeyUrl}{EC}
            port = {CM}{sshPort}{EC}
  
    docker-ssh container name : {CM}{DOCKERSSH_CONTAINER_NAME}{EC}
  docker-rsync container name : {CM}{DOCKERRSYNC_CONTAINER_NAME}{EC}
  
'''.format(
  CM=CM, EC=EC,
  CONTAINER_NAME=CONTAINER_NAME,
  DOCKERSSH_CONTAINER_NAME=getDockerSshName(CONTAINER_NAME),
  DOCKERRSYNC_CONTAINER_NAME=getDockerRsyncName(CONTAINER_NAME),

  sshPort=getSshKeyPort(CONTAINER_NAME)[1],
  sshKeyUrl=getSshKeyURL(CONTAINER_NAME),
  ENUJ_PHYSICAL_IP=ENUJ_PHYSICAL_IP,
)


steps = '''
{CM}#ssh info{EC}
{step_printSSHSyntax}

{CM}#rsync info{EC}
{step_printRSYNCSyntax}
'''.format(
  CM=CM, EC=EC,
  step_printSSHSyntax=step_printSSHSyntax(CONTAINER_NAME),
  step_printRSYNCSyntax=step_printRSYNCSyntax(CONTAINER_NAME),
)

print(infos)

if not isAutorun:  #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
