#!/usr/bin/env python2.7
pass

#ref. https://trello.com/c/zN2G3q86
pass

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:c:b:p:',
  longOpts  = ['autorun=', 'container', 'browser=', 'port'],
)

isAutorun = getArg('-a', options)
CONTAINER_NAME = getArg('-c', options)
CONTAINER_PORT = getArg('-p', options)
BROWSER = getArg('-b', options) #sample values as ch-chrome, ff-firefox, etc.

#broswer => docker image for the hub
if False: pass
elif BROWSER=='ch':
  DIMG_SELENIUM_HUB = 'selenium/standalone-chrome:3.4.0-einsteinium'
elif BROWSER=='ff':
  DIMG_SELENIUM_HUB = 'selenium/standalone-firefox:3.4.0-einsteinium'
else:
  raise Exception('Unsupported browser "%s"' % BROWSER)

#default container name if not defined
if not CONTAINER_NAME: CONTAINER_NAME = 'selenium-hub-standalone-%s' % BROWSER
SELENIUM_HUB=CONTAINER_NAME

if not CONTAINER_PORT: CONTAINER_PORT='4444'

#endregion parse params


#region print infos & steps

infos='''
#Creating selenium grid w/ standalone hub w/ Chrome
'''.format(
  CM=CM,EC=EC,
)

steps='''
{CM}#start the hub{EC}
docker run -d --name {SELENIUM_HUB} -p {CONTAINER_PORT}:4444 -v /dev/shm:/dev/shm {DIMG_SELENIUM_HUB}

{CM}#wait for the container to come up{EC}
sleep 2

{CM}#aftermath check{EC}
echo
echo 'Aftermath grep check at {eCM}{gridConsole}{eEC}'
#param@curl -s for silent progress
#param@grep -o for only matched result  -P perl expression
curl -s {gridConsole} | grep -o -P ".{{0,11}}{AFTM_00}.{{0,15}}"
curl -s {gridConsole} | grep -o -P ".{{0,55}}{AFTM_01}.{{0,22}}"
echo
echo 'Above list should be {eCM}NOT empty{eEC} i.e. we should see {AFTM_00}, {AFTM_01}, etc.'

{CM}#simple selenium test @ google search{EC}

'''.format(
  CM=CM, EC=EC, eCM=eCM, eEC=eEC,
  SELENIUM_HUB=SELENIUM_HUB,
  CONTAINER_PORT=CONTAINER_PORT,
  DIMG_SELENIUM_HUB=DIMG_SELENIUM_HUB,

  AFTM_00='Standalone',
  AFTM_01='/wd/hub',
  gridConsole='http://localhost:%s/wd/console' % CONTAINER_PORT,
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
