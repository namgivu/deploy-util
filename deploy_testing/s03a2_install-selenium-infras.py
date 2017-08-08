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


#region print infos & steps
steps='''
mkdir -p $HOME/.cache
sudo -H  pip install selenium  #automation-testing framework
sudo -H  pip install pyvirtualdisplay #required Xvfb when running on Ubuntu Server

{CM}#print note to install later{EC}
echo "We will also install other required pip packages via requirements.txt file in git code"
'''.format(
  CM=CM,EC=EC,
)

print(steps)
#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
