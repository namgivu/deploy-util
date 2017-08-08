#!/usr/bin/env python2.7
pass

#ref. https://trello.com/c/zN2G3q86
pass

#load config package
from config import *

#region parse params
pass

options = dict(
  shortOpts='a:h:n:',
  longOpts=['autorun=', 'hubName=', 'nodePrefix',],
)

isAutorun = getArg('-a', options)
SELENIUM_HUB = getArg('-h', options)
SELENIUM_NODE_PREFIX = getArg('-n', options)

if not SELENIUM_HUB:          SELENIUM_HUB = 'selenium-hub'
if not SELENIUM_NODE_PREFIX:  SELENIUM_NODE_PREFIX = 'selenium-node'

pass
#endregion parse params


#prepare hub+node names
HUB_NAME = SELENIUM_HUB
NODE_NAME_CH = '%s-ch' % SELENIUM_NODE_PREFIX
NODE_NAME_FF = '%s-ff' % SELENIUM_NODE_PREFIX


#region print infos & steps

infos = '''
#Clear all containers of selenium grid
'''.format(
)


steps = '''
{CM}#delete the grid{EC}
docker rm -f $(docker ps -qa -f name={HUB_NAME} -f name={NODE_NAME_CH} -f name={NODE_NAME_FF})
'''.format(
  CM=CM, EC=EC,

  HUB_NAME=HUB_NAME,
  NODE_NAME_CH=NODE_NAME_CH,
  NODE_NAME_FF=NODE_NAME_FF,
)


print(infos)

if not isAutorun:  #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
