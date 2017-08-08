#!/usr/bin/env python2.7

from common import * #initiate common asset
from input  import * #load the inputs

#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options)
#endregion parse params

autorun='-a 1' if isAutorun else ''
stepName='remote git pull'
stepFiles='01z_applied.py:04c_git_pull.py'

steps='''
  {DEPLOY_HOME}/08_remote_STEP.py {autorun} -n '{stepName}' -f '{stepFiles}'
'''.format(
  DEPLOY_HOME=DEPLOY_HOME,
  autorun=autorun,
  stepName=stepName,
  stepFiles=stepFiles,
)

print(steps)
#endregion print infos & steps


#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline=''
)
