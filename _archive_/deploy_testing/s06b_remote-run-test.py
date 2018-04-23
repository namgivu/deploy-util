#!/usr/bin/env python2.7
pass


#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options) #TODO Why passing --autorun=1 NOT working, while --verbose=1 works?
#endregion parse params


autorun='-a 1' if isAutorun else ''
stepName  = 'remote s05_run-test'
stepHome  = 'deploy_testing'
stepFiles = 's04z_load-local-config.py:s05_run-test.py'

steps='''
{CM}#Command to run{EC}
{DEPLOY_COMMON_HOME}/s08_remote_STEP.py {autorun} -n '{stepName}' -h '{stepHome}' -f '{stepFiles}'
'''.format(
  CM=CM,EC=EC,
  DEPLOY_COMMON_HOME=DEPLOY_COMMON_HOME,
  autorun=autorun,
  stepName=stepName,
  stepFiles=stepFiles,
  stepHome=stepHome,
)

if not isAutorun:
  print(steps)
#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
