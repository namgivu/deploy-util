#!/usr/bin/env python2.7

#load config package
from config import *


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
{CM}#remote's host info{EC}
  HOST_SSH_KEY = {printedHOST_SSH_KEY}
     HOST_USER = {HOST_USER}
       HOST_IP = {HOST_IP}
 HOST_SSH_PORT = {HOST_SSH_PORT}
     
{CM}#remote's command to run{EC}
runCmd = {runCmd}
'''.format(
  HL=HL,CM=CM,EC=EC,

  printedHOST_SSH_KEY=HOST_SSH_KEY if HOST_SSH_KEY else HOST_SSH_KEY_URL,
  HOST_USER=HOST_USER,
  HOST_IP=HOST_IP,
  HOST_SSH_PORT=HOST_SSH_PORT if HOST_SSH_PORT else '(default port)',

  runCmd=runCmd if runCmd else 'None',
)


#region prepare ssh key
import sys ; sys.stdout.write('Checking SSH key... ') ; sys.stdout.flush() #print without newline ref. https://stackoverflow.com/a/493399/248616
sshKeyCmd = 'sshKey=%s' % HOST_SSH_KEY if HOST_SSH_KEY else \
            'keyUrl="%s" ; keyFile=$(mktemp) ; wget -O $keyFile -q $keyUrl ; sshKey=$keyFile #download key' % HOST_SSH_KEY_URL
print('DONE')

assert sshKeyCmd is not None, 'HOST_SSH_KEY is required'
#endregion prepare ssh key


steps='''
{CM}#run below command to ssh-connect{EC}
{sshKeyCmd}
eval $(ssh-agent -s) > /dev/null
ssh-add $sshKey > /dev/null
ssh {verbose} -i $sshKey -o '{autoAccept}' -t {hostAtIP} {port} "{runCmd}"
'''.format(
  HL=HL,CM=CM,EC=EC,
  verbose=verbose,
  sshKeyCmd=sshKeyCmd,
  autoAccept='StrictHostKeyChecking no', #auto accept key

  hostAtIP='{HOST_USER}@{HOST_IP}'.format(HOST_USER=HOST_USER,  HOST_IP=HOST_IP) \
           if HOST_USER else HOST_IP,
  port='-p %s' % HOST_SSH_PORT if HOST_SSH_PORT else '',
  runCmd=runCmd,
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps

if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
