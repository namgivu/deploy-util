#!/usr/bin/env python2.7
pass

#ref. https://trello.com/c/zN2G3q86
pass

#load config package
from config import *

#region parse params
pass

options = dict(
  shortOpts='a:h:n:p:s:x:',
  longOpts=['autorun=', 'hubName=', 'nodePrefix', 'port', 'scaleParams', 'gridNamePrefix'],
)

isAutorun = getArg('-a', options)

SELENIUM_HUB = getArg('-h', options)
SELENIUM_NODE_PREFIX = getArg('-n', options)
CONTAINER_PORT = getArg('-p', options)

SCALE_PARAMS = getArg('-s', options)
GRID_NAME_PREFIX = getArg('-x', options) #TODO Make this as an input entry instead of param

if not SELENIUM_HUB:          SELENIUM_HUB = 'selenium-hub'
if not SELENIUM_NODE_PREFIX:  SELENIUM_NODE_PREFIX = 'selenium-node'
if not CONTAINER_PORT:        CONTAINER_PORT = '4444'
if not GRID_NAME_PREFIX:      GRID_NAME_PREFIX = 'enuj'  #docker-compose container name prefix

#endregion parse params


DIMG_SELENIUM_HUB     = 'selenium/hub:3.4.0-einsteinium'          #or 'selenium/hub'
DIMG_SELENIUM_NODE_CH = 'selenium/node-chrome:3.4.0-einsteinium'  #or 'selenium/node-chrome'
DIMG_SELENIUM_NODE_FF = 'selenium/node-firefox:3.4.0-einsteinium' #or 'selenium/node-firefox'

pass
#region print infos & steps

infos = '''
#Create scalable selenium grid
'''.format(
)


#prepare docker_compose.yml file
if 'ENUJ_VAULT' not in locals(): #check if variable defined ref. https://stackoverflow.com/a/843293/248616
  ENUJ_VAULT = '/tmp' #if not defined, we put it into the /tmp
DOCKER_COMPOSE_FILE = '%s/docker-compose.yml' % ENUJ_VAULT

#prepare hub+node names
HUB_NAME = SELENIUM_HUB
NODE_NAME_CH = '%s-ch' % SELENIUM_NODE_PREFIX
NODE_NAME_FF = '%s-ff' % SELENIUM_NODE_PREFIX

#hub port
HUB_PORT = CONTAINER_PORT

#node scale default as ch=2 ff=1
if not SCALE_PARAMS:
  SCALE_PARAMS = '--scale {NODE_NAME_CH}=2 --scale {NODE_NAME_FF}=1'.format(
    NODE_NAME_CH=NODE_NAME_CH,
    NODE_NAME_FF=NODE_NAME_FF,
  )


steps=''

steps+='''
{CM}#create docker_compose.yml{EC}
cat <<EOT > {DOCKER_COMPOSE_FILE}
{HUB_NAME}:
  image: {DIMG_SELENIUM_HUB}
  ports:
    - 4444:4444
  restart: always #TODO consider to put this in ref. https://gist.github.com/manoj9788/67e248064c89d622cadc6192c66b184d


{NODE_NAME_CH}:
  image: {DIMG_SELENIUM_NODE_CH}
  ports:
    - 5900 #may help in case of some single node restarts or more advance configurations e.g. distributed
  links:
    - {HUB_NAME}:hub
  restart: always #TODO consider to put this in ref. https://gist.github.com/manoj9788/67e248064c89d622cadc6192c66b184d

{NODE_NAME_FF}:
  image: {DIMG_SELENIUM_NODE_FF}
  ports:
    - 5900 #may help in case of some single node restarts or more advance configurations e.g. distributed
  links:
    - {HUB_NAME}:hub
  restart: always #TODO consider to put this in ref. https://gist.github.com/manoj9788/67e248064c89d622cadc6192c66b184d
EOT
'''.format(
  CM=CM, EC=EC,

  DOCKER_COMPOSE_FILE=DOCKER_COMPOSE_FILE,

  HUB_NAME=HUB_NAME,
  NODE_NAME_CH=NODE_NAME_CH,
  NODE_NAME_FF=NODE_NAME_FF,

  DIMG_SELENIUM_HUB=DIMG_SELENIUM_HUB,
  DIMG_SELENIUM_NODE_CH=DIMG_SELENIUM_NODE_CH,
  DIMG_SELENIUM_NODE_FF=DIMG_SELENIUM_NODE_FF,
)


steps+='''
{CM}#do create{EC}
docker-compose -f {DOCKER_COMPOSE_FILE} -p '{GRID_NAME_PREFIX}'  up -d --force-recreate --remove-orphans {SCALE_PARAMS} #1st-time create; we will scale later #param -p is project name prefix ref. https://stackoverflow.com/a/41222926/248616
cd $currDir
'''.format(
  CM=CM, EC=EC,

  DOCKER_COMPOSE_FILE=DOCKER_COMPOSE_FILE,
  GRID_NAME_PREFIX=GRID_NAME_PREFIX,
  SCALE_PARAMS=SCALE_PARAMS,
)


steps+='''
{CM}#print guideline{EC}
echo "
{eCM}Open selenium console at{eEC}
{gridConsole}

{eCM}#delete this grid{eEC}
docker rm -f \$(docker ps -qa -f name={HUB_NAME} -f name={NODE_NAME_CH} -f name={NODE_NAME_FF})
# docker rm -f \$(docker ps -qa) #or all
 
{eER}#scale up this grid{eEC}
docker-compose -f {DOCKER_COMPOSE_FILE} -p '{GRID_NAME_PREFIX}'  up -d --force-recreate --remove-orphans {SCALE_PARAMS} #create with scale
"
'''.format(
  CM=CM, EC=EC, eCM=eCM, eEC=eEC, eER=eER,

  DOCKER_COMPOSE_FILE=DOCKER_COMPOSE_FILE,

  GRID_NAME_PREFIX=GRID_NAME_PREFIX,
  HUB_NAME=HUB_NAME,
  NODE_NAME_CH=NODE_NAME_CH,
  NODE_NAME_FF=NODE_NAME_FF,

  SCALE_PARAMS=SCALE_PARAMS,

  gridConsole='http://localhost:%s/grid/console' % HUB_PORT,
)


steps+='''
{CM}#aftermath check{EC}
echo "
{eCM}Created hub+nodes{eEC}"
docker ps -f name={HUB_NAME} -f name={NODE_NAME_CH} -f name={NODE_NAME_FF}
'''.format(
  CM=CM, EC=EC, eCM=eCM, eEC=eEC, eER=eER,

  HUB_NAME=HUB_NAME,
  NODE_NAME_CH=NODE_NAME_CH,
  NODE_NAME_FF=NODE_NAME_FF,
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
