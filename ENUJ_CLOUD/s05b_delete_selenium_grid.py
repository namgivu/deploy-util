#!/usr/bin/env python2.7
pass

#ref. https://trello.com/c/zN2G3q86
pass

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:h:n:',
  longOpts  = ['autorun=', 'hubName=', 'nodePrefix='],
)

isAutorun = getArg('-a', options)
SELENIUM_HUB = getArg('-h', options)
SELENIUM_NODE_PREFIX = getArg('-n', options)

if not SELENIUM_HUB: SELENIUM_HUB='selenium-hub'
if not SELENIUM_NODE_PREFIX: SELENIUM_NODE_PREFIX='selenium-node'

#endregion parse params


#region print infos & steps

infos='''
#Deleting selenium grid
'''

steps='''
{CM}#delete the grid{EC}
docker rm -f {SELENIUM_HUB}
docker rm -f {SELENIUM_NODE_PREFIX}-ch
docker rm -f {SELENIUM_NODE_PREFIX}-ff
'''.format(
  CM=CM, EC=EC,
  SELENIUM_HUB=SELENIUM_HUB,
  SELENIUM_NODE_PREFIX=SELENIUM_NODE_PREFIX,
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
