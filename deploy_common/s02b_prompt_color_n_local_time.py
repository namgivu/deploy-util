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

#region print steps
steps='''
#Installing helpful utility... BEGIN

  {CM}#1.prompt color {EC}
  {BASH_UTIL}/prompt-color.sh

  {CM}#2.local time zone {EC}
  {BASH_UTIL}/timezone-ubuntu.sh

#Installing helpful utility... END
'''.format(
  HL=HL,CM=CM,EC=EC,
  BASH_UTIL=BASH_UTIL,
)

print(steps)
#endregion print steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun helpful utility via %s' % os.path.basename(__file__)
)
