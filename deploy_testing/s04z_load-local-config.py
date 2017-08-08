#!/usr/bin/env python2.7

#load config package
from config import *

#region parse params
options = dict(
  shortOpts='a:',
  longOpts=['autorun='],
)

isAutorun = getArg('-a', options)  #TODO Why passing --autorun=1 NOT working, while --verbose=1 works?
#endregion parse params


#region print infos & steps

LOCAL_CONFIG_FROM = '{UTILITY_ROOT}/deploy_testing/config/config_local.py'.format(
  UTILITY_ROOT=UTILITY_ROOT,
)

LOCAL_CONFIG_TO = '{CODE_HOME}/config_local.py'.format(
  CODE_HOME=CODE_HOME,
)


infos = '''
{CM}#local config info{EC}
from {LOCAL_CONFIG_FROM}
to   {LOCAL_CONFIG_TO}
'''.format(
  HL=HL, CM=CM, EC=EC,
  LOCAL_CONFIG_FROM=LOCAL_CONFIG_FROM,
  LOCAL_CONFIG_TO=LOCAL_CONFIG_TO,
)


steps = '''
{CM}#copy/plug in the local config{EC}
cp -f {LOCAL_CONFIG_FROM} {LOCAL_CONFIG_TO}
'''.format(
  HL=HL, CM=CM, EC=EC,
  LOCAL_CONFIG_FROM=LOCAL_CONFIG_FROM,
  LOCAL_CONFIG_TO=LOCAL_CONFIG_TO,
)

print(infos)

if not isAutorun:  #print steps only when not autorun
  print(steps)

#endregion print infos & steps

if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
