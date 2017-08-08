#!/usr/bin/env python2.7

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:c:',
  longOpts  = ['autorun=', 'container='],
)

isAutorun = getArg('-a', options)
CONTAINER_NAME_or_ID = getArg('-c', options)
if not CONTAINER_NAME_or_ID: raise Exception('-c param is required i.e. CONTAINER_NAME_or_ID')

#endregion parse params


#region print infos & steps

infos='''
Terminate a Docker container via its name or id
  container identity : {CM}{CONTAINER_NAME_or_ID}{EC}
'''.format(
  CM=CM,EC=EC,
  CONTAINER_NAME_or_ID=CONTAINER_NAME_or_ID,
)

steps=step_terminateContainer(CONTAINER_NAME_or_ID)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
