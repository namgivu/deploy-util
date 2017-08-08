#!/usr/bin/env python2.7

from config import * #initiate common asset
from input  import * #load the inputs

#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options)
#endregion parse params

#region print infos & steps
infos='''
'''.format(
  HL=HL,CM=CM,EC=EC,
)

steps='''
'''.format(
  HL=HL,CM=CM,EC=EC,
)

print(infos)
print(steps)
#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun YOUR_STEPS'
)
