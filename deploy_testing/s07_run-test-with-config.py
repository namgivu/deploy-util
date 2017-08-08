#!/usr/bin/env python2.7

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:c:',
  longOpts  = ['autorun=','configFile'],
)

isAutorun   = getArg('-a', options) #TODO Why passing --autorun=1 NOT working, while --verbose=1 works?
configFile  = getArg('-c', options) #the custom config file name under 'config' folder

if not configFile: configFile='config_local.py'
#endregion parse params


RUN_TEST = '%s/s01.run-test.sh' % CODE_HOME


#region print infos & steps

LOCAL_CONFIG_FROM = '{DEPLOY_TESTING_HOME}/config/{configFile}'.format(
  DEPLOY_TESTING_HOME=DEPLOY_TESTING_HOME,
  configFile=configFile,
)

LOCAL_CONFIG_TO = '{CODE_HOME}/config_local.py'.format(
  CODE_HOME=CODE_HOME,
)


infos = '''
Config info
from {CM}{LOCAL_CONFIG_FROM}{EC}
to   {CM}{LOCAL_CONFIG_TO}{EC}
'''.format(
  HL=HL, CM=CM, EC=EC,
  LOCAL_CONFIG_FROM=LOCAL_CONFIG_FROM,
  LOCAL_CONFIG_TO=LOCAL_CONFIG_TO,
)


steps = '''
{CM}#copy/plug in the local config{EC}
cp -f {LOCAL_CONFIG_FROM} {LOCAL_CONFIG_TO}

{CM}#run below command to start the test{EC}
{RUN_TEST}
'''.format(
  HL=HL,CM=CM,EC=EC,
  LOCAL_CONFIG_FROM=LOCAL_CONFIG_FROM,
  LOCAL_CONFIG_TO=LOCAL_CONFIG_TO,
  RUN_TEST=RUN_TEST,
)


print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps

if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
