#!/usr/bin/env python2.7
pass

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:p:c:i:',
  longOpts  = ['autorun=', 'port=', 'container', 'containerImage'],
)

isAutorun = getArg('-a', options)

#TODO rsync port to be selected automatically as 22xx ref. https://stackoverflow.com/q/44940239/248616
CONTAINER_RSYNC_PORT = getArg('-p', options)
CONTAINER_NAME = getArg('-c', options)
CONTAINER_IMAGE = getArg('-i', options)

if not CONTAINER_NAME: raise Exception('CONTAINER_NAME is required ')
if not CONTAINER_IMAGE: raise Exception('CONTAINER_IMAGE is required ')
if not CONTAINER_RSYNC_PORT: raise Exception('CONTAINER_RSYNC_PORT is required ')
#endregion parse params


#region print infos & steps

DOCKER_RSYNC_NAME = 'docker-rsync_%s_%s' % (CONTAINER_RSYNC_PORT, CONTAINER_NAME) #force to use container name i.e. if IP is given, parse the name from it

infos = '''
Create rsync chanel to a Docker container via nabeken/docker-volume-container-rsync ref. https://github.com/nabeken/docker-volume-container-rsync
        parent container name : {CM}{CONTAINER_NAME}{EC}
  docker-rsync container name : {CM}{DOCKER_RSYNC_NAME}{EC}
'''.format(
  CM=CM, EC=EC,
  CONTAINER_NAME=CONTAINER_NAME,
  DOCKER_RSYNC_NAME=DOCKER_RSYNC_NAME,
)


steps='''
{CM}#start nabeken image with setup param to rsync to remote $HOME e.g. /root, /home/seluser, etc. {EC}
docker run -d  -p {CONTAINER_RSYNC_PORT}:873  --volume {REMOTE_RSYNC_HOME} -e VOLUME={REMOTE_RSYNC_HOME}  --name {DOCKER_RSYNC_NAME}  nabeken/docker-volume-container-rsync:latest
echo
docker ps -f name=^/{DOCKER_RSYNC_NAME} #print container info 

{CM}#aftermath test - ls the volume folder{EC}
echo
echo 'The created volume content as below'
rsync rsync://{ENUJ_PHYSICAL_IP}:{CONTAINER_RSYNC_PORT}/volume

#Attach the volume to target container '{CONTAINER_NAME}'
#docker run -it -d --name {CONTAINER_NAME} --volumes-from {DOCKER_RSYNC_NAME} ubuntu:16.04 bash
#From now on, use the below command syntax to rsync
#rsync -chazk $autonomous_utility rsync://{ENUJ_PHYSICAL_IP}:{CONTAINER_RSYNC_PORT}/volume/$DEPLOY_ID

{CM}#print rsync command guide{EC}
echo '
{eCM}#Command to rsync to container '{CONTAINER_NAME}' {eEC}
rsync -chazk $YOUR_LOCAL_FOLDER/ rsync://{ENUJ_PHYSICAL_IP}:{CONTAINER_RSYNC_PORT}/volume/$SUBPATH_IN_HOME
'
'''.format(
  CM=CM, EC=EC,  eCM=eCM, eEC=eEC,
  CONTAINER_RSYNC_PORT=CONTAINER_RSYNC_PORT,
  REMOTE_RSYNC_HOME=getUserHome_fromImageName(CONTAINER_IMAGE),
  DOCKER_RSYNC_NAME=DOCKER_RSYNC_NAME,
  CONTAINER_NAME=CONTAINER_NAME,
  ENUJ_PHYSICAL_IP=ENUJ_PHYSICAL_IP,
)


print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
