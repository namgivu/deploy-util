#!/usr/bin/env python2.7

from common   import * #initiate common asset
from input    import * #load the inputs

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

  {HL}#1.prompt color {EC}
  {BASH_UTIL}/prompt-color.sh

  {HL}#2.local time zone {EC}
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
  steps, headline='Autorun installing helpful utility'
)
