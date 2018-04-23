#!/usr/bin/env python2.7
pass

#load config package
from config import *

#region parse params
options = dict(
  shortOpts = 'a:c:i:s:r:',
  longOpts  = ['autorun=','containerName','sshPort','rsyncPort'],
)

isAutorun = getArg('-a', options) #TODO Why passing --autorun=1 NOT working, while --verbose=1 works?
containerName   = getArg('-c', options)
containerImage  = getArg('-i', options)
sshPort   = getArg('-s', options)
rsyncPort = getArg('-r', options)
#endregion parse params


containerName = containerName if containerName else 'autotest'
sshPort       = sshPort if sshPort else '22000'
rsyncPort     = rsyncPort if rsyncPort else '18000'


#region print infos & steps

infos=''


def defineSteps():
  return '''
  export       ENUJ_CONTAINER_NAME={CM}{containerName}{EC}
  export   ENUJ_CONTAINER_SSH_PORT={CM}{sshPort}{EC} #22xxx 22 the SSH port
  export ENUJ_CONTAINER_RSYNC_PORT={CM}{rsyncPort}{EC} #18xxx 18=8+7+3 i.e. 873 the rsync port
  
  export ENUJ_CLOUD_HOME={ENUJ_CLOUD_HOME} ; e=$ENUJ_CLOUD_HOME
  export UTILITY_ROOT={UTILITY_ROOT}
  
  {CM}#docker image choice{EC}  
  export ENUJ_CONTAINER_IMAGE={CM}{containerImage00}{EC}
  export ENUJ_CONTAINER_IMAGE={CM}{containerImage01}{EC}
  '''.format(
    CM=CM,EC=EC,

    ENUJ_CLOUD_HOME=ENUJ_CLOUD_HOME,
    UTILITY_ROOT=UTILITY_ROOT,

    containerName=containerName,
    containerImage00=EnujDockerImage.UBUNTU_1604,
    containerImage01=EnujDockerImage.DOCKER_SELENIUM_HUB,
    sshPort=sshPort,
    rsyncPort=rsyncPort,
  ).rstrip()


def atomSteps():
  return '''
  sudo echo 'sudo initiated'

  {CM}#create container{EC}
  $e/s01a_create_rsync_container.py -c $ENUJ_CONTAINER_NAME -p $ENUJ_CONTAINER_RSYNC_PORT -i $ENUJ_CONTAINER_IMAGE -a 1
  
  #TODO Shall we make it a docker stack for those 3 containers to run a node?
  $e/s01b01_create_container_UBUNTU.py -c $ENUJ_CONTAINER_NAME -a 1
  $e/s01b02_create_container_DOCKER_SELENIUM.py -c $ENUJ_CONTAINER_NAME -a 1

  $e/s01c_create_ssh_container.py -c $ENUJ_CONTAINER_NAME -p $ENUJ_CONTAINER_SSH_PORT -a 1
  
  {CM}#install utility{EC}
  $e/s02c1_apt_update_sudo.py -c $ENUJ_CONTAINER_NAME -a 1 #may having long execution time
  $e/s02c2_custom_bash.py -c $ENUJ_CONTAINER_NAME -a 1
  
  {CM}#terminate container{EC}
  sudo echo 'sudo initiated'
  $e/s03a_terminate_ssh_container.py -c $ENUJ_CONTAINER_NAME -a 1
  $e/s03b_terminate_rsync_container.py -c $ENUJ_CONTAINER_NAME -a 1
  $e/s03c_terminate_container.py -c $ENUJ_CONTAINER_NAME -a 1
'''.format(
  HL=HL,CM=CM,EC=EC,
).rstrip()


def featureSteps():
  return '''
  sudo echo 'sudo initiated'

  {CM}#create enuj node{EC}
  $e/s04a_create_node.py -c $ENUJ_CONTAINER_NAME -i $ENUJ_CONTAINER_IMAGE -s $ENUJ_CONTAINER_SSH_PORT -r $ENUJ_CONTAINER_RSYNC_PORT -a 1

  #(optional) update apt-get repo and install sudo
  $e/s02c1_apt_update_sudo.py -c $ENUJ_CONTAINER_NAME -a 1

  #(optional) customize bash e.g. prompt color, ls with color, etc.
  $e/s02c2_custom_bash.py -c $ENUJ_CONTAINER_NAME -a 1


  {CM}#delete enuj node{EC}
  $e/s04c_delete_node.py -c $ENUJ_CONTAINER_NAME -a 1
  '''.format(
    HL=HL, CM=CM, EC=EC,
  ).rstrip()


def usageGuide():
  return '''
  {CM}#all{EC}
  $e/s04b_print_node.py -c $ENUJ_CONTAINER_NAME -a 1

  {CM}#ssh{EC}
  $e/s02a_ssh_connect.py -c $ENUJ_CONTAINER_NAME -a 1

  {CM}#rsync{EC}
  export ENUJ_RSYNC_FROM={ENUJ_RSYNC_FROM}/
  export ENUJ_RSYNC_TO={ENUJ_RSYNC_TO}
  
  #rsync bash-style way
  rsync -chazkP $ENUJ_RSYNC_FROM rsync://{ENUJ_PHYSICAL_IP}:{containerRsyncPort}/volume/$ENUJ_RSYNC_TO #do rsync
  rsync rsync://{ENUJ_PHYSICAL_IP}:{containerRsyncPort}/volume/$ENUJ_RSYNC_TO #aftermath check i.e. remote folder listing

  #rsync enuj-style way
  export ENUJ_RSYNC_PRUNE='deploy_mysql:deploy_flask:deploy_brain:_daily_:ENUJ_CLOUD  :venv:.git*:.idea:88_YOUR_STEP.py'
  $e/s02b_rsync_util.py -c $ENUJ_CONTAINER_NAME -f $ENUJ_RSYNC_FROM/ -t $ENUJ_RSYNC_TO -p $ENUJ_RSYNC_PRUNE -a 1
  '''.format(
    HL=HL, CM=CM, EC=EC,
    ENUJ_RSYNC_FROM=UTILITY_ROOT,
    ENUJ_RSYNC_TO='autotest.aos-web.ENUJ',
    ENUJ_PHYSICAL_IP=ENUJ_PHYSICAL_IP,
    containerRsyncPort=rsyncPort,
  ).rstrip()


steps='''
{ER}#clear every thing{EC}
#$UTILITY_ROOT/util/bash_util/docker_util/clear-docker-container.sh

{HL}#define enuj node{EC}
{defineSteps}
  
{HL}#atom steps{EC}
{atomSteps}

{HL}#feature steps{EC}
{featureSteps}

{HL}#usage command guide{EC}
{usageGuide}
'''.format(
  ER=ER,HL=HL,CM=CM,EC=EC,

  defineSteps=defineSteps(),
  atomSteps=atomSteps(),
  featureSteps=featureSteps(),
  usageGuide=usageGuide(),
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps

if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
