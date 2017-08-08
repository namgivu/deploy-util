#!/usr/bin/env python2.7

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options) #TODO Why passing --autorun=1 NOT working, while --verbose=1 works?
#endregion parse params


RUN_TEST    = '%s/s01.run-test.sh'    % CODE_HOME


#region print infos & steps

steps='''
{CM}#run below command to start the test{EC}
{RUN_TEST}
'''.format(
  HL=HL,CM=CM,EC=EC,
  RUN_TEST=RUN_TEST,
)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps

if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
