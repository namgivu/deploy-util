#!/usr/bin/env python2.7

from common import * #initiate common asset
from input  import * #load the inputs

#region parse params
options = dict(
  shortOpts = 'a:n:f:',
  longOpts  = ['autorun=', 'stepName=', 'stepFiles='],
)

isAutorun = getArg('-a', options)
stepName  = getArg('-n', options)
stepFiles = getArg('-f', options)
#endregion parse params

#region input validate
if not stepName: stepName = 'remote step'
#endregion input validate

#region print infos & steps
REMOTE_DEPLOY_HOME = '{REMOTE_HOME_bash}/deploy.{DEPLOY_ID}'.format(
  REMOTE_HOME_bash=REMOTE_HOME_bash,
  DEPLOY_ID=DEPLOY_ID,
)
STEPS_HOME='%s/deploy_flask/steps' % REMOTE_DEPLOY_HOME
autorun='-a 1'

#region parse step files
splited = stepFiles.split(':')


remoteSteps = ''
for stepFile in splited:
  remoteSteps += '{STEPS_HOME}/{stepFile} {autorun};'.format(
    STEPS_HOME=STEPS_HOME,
    stepFile=stepFile.strip(),
    autorun=autorun,
  )
#endregion parse step files

steps='''
{HL}#Remote execution commands in 'remoteSteps' {EC}
  {DEPLOY_HOME}/00_ssh_connect.py --command='{remoteSteps}' {autorun}
'''.format(
  HL=HL,CM=CM,EC=EC,
  DEPLOY_HOME=DEPLOY_HOME,
  remoteSteps=remoteSteps,
  autorun=autorun,
)

print(steps)
#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % stepName
)
