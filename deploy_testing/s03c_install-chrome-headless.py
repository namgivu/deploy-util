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
"""ref. https://www.tecmint.com/install-google-chrome-in-debian-ubuntu-linux-mint"""
steps='''
{CM}#add chrome beta to apt-repo{EC}
  #Download the key and then use apt-key to add it to the system
  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

  #After adding the key, run the following command to add chrome repository to your system sources
  sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

  #After adding chrome repository, you must do a system update to update the newly added chrome repository
  echo "\n{eCM}updating apt-get repo{eEC}"
  sudo apt-get update

{CM}#region install chrome 59+ from beta channel{EC}
  #Install Chrome Beta Version
  echo "\n{eCM}installing chrome beta...{eEC}"
  sudo apt-get update
  sudo apt-get install -y google-chrome-beta

{CM}#aftermath check{EC}
echo "
  {eCM}#Chrome 59+ version check{eEC}
  google-chrome-beta  --version
  `google-chrome-beta --version`
"
'''.format(
  CM=CM,EC=EC,
  eCM=eCM,eEC=eEC,
  PIP_REQUIREMENT=PIP_REQUIREMENT,
)

print(steps)
#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
