#!/usr/bin/env python2.7

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options)
#endregion parse params


#region print infos & steps

infos='''
Installing Docker infrastructure
'''.format(
)

steps='''
{CM}#install docker{EC}
{DOCKER_BASH_UTIL}/install-docker.sh

{CM}#install docker-compose{EC}
{DOCKER_BASH_UTIL}/install-docker-compose.sh

{CM}#install monitor util 'htop' {EC}
sudo apt get install -y htop

'''.format(
  CM=CM, EC=EC,
  DOCKER_BASH_UTIL=DOCKER_BASH_UTIL,
  BASH_UTIL=BASH_UTIL,
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
