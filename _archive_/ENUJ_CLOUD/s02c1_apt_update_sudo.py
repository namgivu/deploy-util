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
assert CONTAINER_NAME_or_ID is not None, '-c param is required i.e. CONTAINER_NAME_or_ID'
CONTAINER_NAME = DockerUtil.getNameOrFail(CONTAINER_NAME_or_ID)

##endregion parse params


#region print infos & steps

infos = '''
'''.format(
)

steps = '''
{CM}#remote run command'{EC}
{ENUJ_CLOUD_HOME}/s02a_ssh_connect.py -c {CONTAINER_NAME} -r "{remoteCmd}" -a 1
'''.format(
  CM=CM, EC=EC,
  ENUJ_CLOUD_HOME=ENUJ_CLOUD_HOME,
  CONTAINER_NAME=CONTAINER_NAME,
  remoteCmd='apt-get update ; apt-get install -y sudo', #install sudo ref. https://stackoverflow.com/a/15596379/248616
)


print(infos)

if not isAutorun:  #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
