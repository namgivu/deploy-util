#!/usr/bin/env python2.7
pass

#We remove this steps since we can setup Xvfb right inside Python code ref. https://stackoverflow.com/a/30103931/248616
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


{CM}#set X-display 's number{EC}
dn=99
XDisplayNumber=":$dn"


{CM}#starting Xvfb{EC}
Xvfb $XDisplayNumber -ac &
export DISPLAY=$XDisplayNumber


{CM}#summary{EC}
echo
echo "{eCM}You are now having an X display by Xvfb number $XDisplayNumber{eEC}"
ps aux | grep "Xvfb $XDisplayNumber"
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
