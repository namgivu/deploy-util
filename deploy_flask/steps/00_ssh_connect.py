#!/usr/bin/env python2.7

#TODO use deploy_common util

from common import * #initiate common asset
from input  import * #load the inputs

#region parse params
options = dict(
  shortOpts = 'a:c:v:',
  longOpts  = ['autorun=', 'command=', 'verbose='],
)

isAutorun = getArg('-a', options) #TODO Why passing --autorun=1 NOT working, while --verbose=1 works?
isVerbose = getArg('-v', options)
runCmd    = getArg('--command', options)
#endregion parse params

#region initial
verbose = '-v' if isVerbose else ''
runCmd = runCmd if runCmd else ''
#endregion initial

#region print infos & steps

infos='''
{HL}#Open SSH Connect BEGIN{EC}

  {CM}#remote's host info{EC}
  HOST_SSH_KEY = {printedHOST_SSH_KEY}
     HOST_USER = {HOST_USER}
       HOST_IP = {HOST_IP}

  {CM}#remote's command to run{EC}
  runCmd = {runCmd}
'''.format(
  HL=HL,CM=CM,EC=EC,

  printedHOST_SSH_KEY=HOST_SSH_KEY if HOST_SSH_KEY else HOST_SSH_KEY_URL,
  HOST_USER=HOST_USER,
  HOST_IP=HOST_IP,

  runCmd=runCmd if runCmd else 'None',
)

sshKey = HOST_SSH_KEY if HOST_SSH_KEY else downloadFile(HOST_SSH_KEY_URL, chmod='600')
steps='''
  {CM}#run below command to ssh-connect{EC}
  export sshKey={sshKey} {downloadedNote}
  eval $(ssh-agent -s) > /dev/null
  ssh-add $sshKey > /dev/null
  ssh {verbose} -i $sshKey -o '{autoAccept}' -t {HOST_USER}@{HOST_IP} "{runCmd}"

{HL}#Open SSH Connect END{EC}
'''.format(
  HL=HL,CM=CM,EC=EC,

  verbose=verbose,
  sshKey=sshKey,
  downloadedNote='#ssh key downloaded to this temp file' if sshKey != HOST_SSH_KEY else '',
  autoAccept='StrictHostKeyChecking no', #auto accept key
  HOST_USER=HOST_USER,
  HOST_IP=HOST_IP,
  runCmd=runCmd,
)

print(infos)
print(steps)

#endregion print infos & steps

if isAutorun: runPrintedSteps(
  steps, headline='Autorun ssh-connect'
)
