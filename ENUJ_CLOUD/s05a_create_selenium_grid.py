#!/usr/bin/env python2.7
pass

#ref. https://trello.com/c/zN2G3q86
pass

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:h:n:p:',
  longOpts  = ['autorun=', 'hubName=', 'nodePrefix', 'port'],
)

isAutorun = getArg('-a', options)
SELENIUM_HUB = getArg('-h', options)
SELENIUM_NODE_PREFIX = getArg('-n', options)
CONTAINER_PORT = getArg('-p', options)

if not SELENIUM_HUB: SELENIUM_HUB='selenium-hub'
if not SELENIUM_NODE_PREFIX: SELENIUM_NODE_PREFIX='selenium-node'
if not CONTAINER_PORT: CONTAINER_PORT='4444'

#endregion parse params


DIMG_SELENIUM_HUB     = 'selenium/hub:3.4.0-einsteinium'          #or 'selenium/hub'
DIMG_SELENIUM_NODE_CH = 'selenium/node-chrome:3.4.0-einsteinium'  #or 'selenium/node-chrome'
DIMG_SELENIUM_NODE_FF = 'selenium/node-firefox:3.4.0-einsteinium' #or 'selenium/node-firefox'


#region print infos & steps

infos='''
#Creating selenium grid
'''.format(
)

steps='''
{CM}#start the hub{EC}
docker run -d --name {SELENIUM_HUB} -p {CONTAINER_PORT}:4444 {DIMG_SELENIUM_HUB}

{CM}#start the node Chrome{EC}
docker run -d --name {SELENIUM_NODE_PREFIX}-ch --link selenium-hub:hub {DIMG_SELENIUM_NODE_CH}

{CM}#start the node Firefox{EC}
docker run -d --name {SELENIUM_NODE_PREFIX}-ff --link selenium-hub:hub {DIMG_SELENIUM_NODE_FF}

{CM}#wait for the container to come up{EC}
sleep 2

{CM}#aftermath check{EC}
echo
echo 'Aftermath grep check at {eCM}{gridConsole}{eEC}'
#param@curl -s for silent progress
#param@grep -o for only matched result  -P perl expression
curl -s {gridConsole} | grep -o -P ".{{0,11}}{AFTM_GridConsole}.{{0,15}}"
curl -s {gridConsole} | grep -o -P ".{{0,55}}{AFTM_Chrome}.{{0,22}}"
curl -s {gridConsole} | grep -o -P ".{{0,55}}{AFTM_Firefox}.{{0,22}}"
echo
echo 'Above list should be {eCM}NOT empty{eEC} i.e. we should see {AFTM_GridConsole}, {AFTM_Chrome}, {AFTM_Firefox}, etc.'
'''.format(
  CM=CM, EC=EC, eCM=eCM, eEC=eEC,
  SELENIUM_HUB=SELENIUM_HUB,
  CONTAINER_PORT=CONTAINER_PORT,
  SELENIUM_NODE_PREFIX=SELENIUM_NODE_PREFIX,

  DIMG_SELENIUM_HUB=DIMG_SELENIUM_HUB,
  DIMG_SELENIUM_NODE_CH=DIMG_SELENIUM_NODE_CH,
  DIMG_SELENIUM_NODE_FF=DIMG_SELENIUM_NODE_FF,

  AFTM_GridConsole='Grid Console',
  AFTM_Chrome='chrome.png',
  AFTM_Firefox='firefox.png',
  gridConsole='http://localhost:%s/grid/console' % CONTAINER_PORT,
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
