#!/usr/bin/env python2.7
pass

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)
isAutorun = getArg('-a', options)
#endregion parse params


#region print infos & steps
"""ref. https://stackoverflow.com/a/10399597/248616"""
steps='''
{CM}#install Xvfb{EC}
sudo apt install -y xvfb
'''.format(
  CM=CM,EC=EC,
  eCM=eCM,eEC=eEC,
)

print(steps)
#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
