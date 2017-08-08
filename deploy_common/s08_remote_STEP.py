#!/usr/bin/env python2.7

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:n:f:h:',
  longOpts  = ['autorun=', 'stepName=', 'stepFiles=', 'stepHome='],
)

isAutorun = getArg('-a', options)
stepName  = getArg('-n', options)
stepFiles = getArg('-f', options)
stepHome  = getArg('-h', options)
#endregion parse params


#region input validate
if not stepName: stepName = 'no-name remote step'
if not stepHome: stepHome = 'deploy_flask'
#endregion input validate

#region print infos & steps1
REMOTE_DEPLOY_HOME = '{REMOTE_HOME_bash}/{DEPLOY_HOME_PREFIX}.{DEPLOY_ID}'.format(  #TODO Combine with REMOTE_UTIL_PATH in 's01z_applied.py'
  DEPLOY_HOME_PREFIX=DEPLOY_HOME_PREFIX,
  REMOTE_HOME_bash=REMOTE_HOME_bash,
  DEPLOY_ID=DEPLOY_ID,
)
STEPS_HOME='{REMOTE_DEPLOY_HOME}/{stepHome}'.format(REMOTE_DEPLOY_HOME=REMOTE_DEPLOY_HOME, stepHome=stepHome)
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
{CM}#Remote execution commands in 'remoteSteps'{EC}
{DEPLOY_COMMON_HOME}/s00_ssh_connect.py --command='{remoteSteps}' {autorun}
'''.format(
  HL=HL,CM=CM,EC=EC,
  DEPLOY_COMMON_HOME=DEPLOY_COMMON_HOME,
  remoteSteps=remoteSteps,
  autorun=autorun,
)

if not isAutorun:
  print(steps)
#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % stepName
)
