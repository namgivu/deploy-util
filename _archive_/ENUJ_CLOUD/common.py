#!/usr/bin/env python2.7
from config import *
from docker_util import *


def randomTag(length=6):
  import uuid
  return uuid.uuid4().get_hex()[0:length] #random string ref. https://stackoverflow.com/a/17323913/248616


#region docker-ssh util
pass


def canSsh(containerName):
  """Check if docker-ssh container is ready for container `name`"""
  return getSshKeyURL(containerName)


def extractPort(sshKeyFile):
  """Extract port from filename at full path `sshKeyFile` """
  import ntpath
  filename = ntpath.basename(sshKeyFile)  # ref. https://stackoverflow.com/a/8384788/248616
  splits = filename.split('_')
  assert len(splits) == 3, 'Invalid filename for ssh key at %s' % sshKeyFile
  port = splits[1]
  return port


def getSshKeyPort(containerName):
  """
  - Get ssh key for container `containerName` i.e. the key been setup with its docker-ssh container
  - The key stored at path `vaultPath`; each docker-ssh container will have 3 key files here
    1) docker-ssh_PORT_NAME
    2) docker-ssh_PORT_NAME.authorized_keys
    2) docker-ssh_PORT_NAME.pub
  """

  # the name must valid first
  if not DockerUtil.validateName(containerName): return None, None

  # search ssh-key vault for this name
  '''check file exists with regex'''
  sshKey = '{ENUJ_SSH_KEY_VAULT}/docker-ssh_*_{containerName}'.format(containerName=containerName, ENUJ_SSH_KEY_VAULT=ENUJ_SSH_KEY_VAULT)
  authKey = '%s.authorized_keys' % sshKey
  pubKey = '%s.pub' % sshKey
  import glob
  sshKeyFILES = glob.glob(sshKey)  # ref. https://stackoverflow.com/a/4296148/248616
  authFILES = glob.glob(authKey)
  pubKeyFILES = glob.glob(pubKey)

  ok = len(sshKeyFILES) == 1 and len(authFILES) == 1 and len(pubKeyFILES) == 1
  assert ok is True, 'Key files error for container %s' % containerName
  keyFile = sshKeyFILES[0] if ok else None
  sshPort = extractPort(sshKeyFile=keyFile) if ok else None

  return keyFile, sshPort


def getDockerSshName(containerName):
  """Get docker-ssh container name from its parent-container's name"""
  sshKeyFile,port = getSshKeyPort(containerName)

  if not sshKeyFile: return None

  import ntpath
  filename = ntpath.basename(sshKeyFile)  # get filename from full path ref. https://stackoverflow.com/a/8384788/248616

  return filename


def getSshKeyURL(containerName):
  """
  - From docker-ssh container name `dockerssh_containerName`, get its ssh-key url
  - Key be searched in folder `publishedVault`
  - URL be created using host at ip `enujIP`
  """
  dockerssh_containerName = getDockerSshName(containerName)
  import glob
  found = glob.glob( #search file ref. https://stackoverflow.com/a/4296148/248616
    '{ENUJ_SSH_KEY_PUBLISHED_VAULT}/{dockerssh_containerName}_*'.format(
      ENUJ_SSH_KEY_PUBLISHED_VAULT=ENUJ_SSH_KEY_PUBLISHED_VAULT,
      dockerssh_containerName=dockerssh_containerName
    )
  )

  assert len(found)<=1, 'Too many key files for container "%s" i.e. %s' % (containerName, found)
  if not found: return None

  import ntpath
  filename = ntpath.basename(found[0]) #get filename from full path ref. https://stackoverflow.com/a/8384788/248616
  url = makeEnujKeyUrl(filename)
  return url


def getDockerRsyncPort(containerName):
  """
  Get docker-rsync mapped port of container name='containerName'
  """

  #the name must valid first
  if not DockerUtil.validateName(containerName): return None

  #extract port from docker-rsync name
  dockerRsyncName = getDockerRsyncName(containerName)
  splits = dockerRsyncName.split('_')
  assert len(splits)==3, 'Invalid container name format "%s" ' % containerName
  port = splits[1]
  return port


def getDockerRsyncName(containerName):
  """Get docker-rsync container name from its parent-container's name"""
  import fnmatch
  for container in DOCKER_CLIENT.containers.list():
    matched = fnmatch.fnmatch( #search string w/ wildcard ref. https://stackoverflow.com/a/11427183/248616
      name=container.name,
      pat='docker-rsync_*_{containerName}'.format(containerName=containerName)
    )
    if matched:
      return container.name

  return None #not found


def makeEnujKeyUrl(filename):
  return 'http://{ENUJ_PHYSICAL_IP}/{ENUJ_PUBLISHED_SUBPATH}/{filename}'.format(
    ENUJ_PHYSICAL_IP=ENUJ_PHYSICAL_IP,
    ENUJ_PUBLISHED_SUBPATH=ENUJ_PUBLISHED_SUBPATH,
    filename=filename,
  )


pass
#endregion docker-ssh util


##region common info & step
pass


def step_terminateContainer(containerName):
  return '''
{CM}#stop docker image{EC}
#docker stop {containerName}  #this won't terminate it right away 
docker rm -f {containerName}  #this one does ref. https://www.ctl.io/developers/blog/post/gracefully-stopping-docker-containers/#docker-rm-f

{CM}#aftermath check{EC}
echo
echo 'Below list must be empty'
docker ps -f name=^/{containerName} #this should print nothing 
'''.format(
  CM=CM, EC=EC,
  containerName=containerName,
  ENUJ_SSH_KEY_VAULT=ENUJ_SSH_KEY_VAULT,
  ENUJ_SSH_KEY_PUBLISHED_VAULT=ENUJ_SSH_KEY_PUBLISHED_VAULT,
)


def info_terminateContainer(parentContainerName, containerName):
  return '''
Terminate a docker-ssh container via its parent container's name
      parent-container name : {CM}{parentContainerName}{EC}
  docker-ssh container name : {CM}{containerName}{EC}
'''.format(
  CM=CM, EC=EC,
  parentContainerName=parentContainerName,
  containerName=containerName,
)


def step_printSshConnectGuide(sshKeyFile, sshPort, sshKeyUrl):
  return '''
{CM}#print guideline on ssh command{EC}
echo '
{eCM}#You now can SSH-connect to the container from this machine{eEC}
ssh -p {sshPort} -i {sshKeyFile} {autoAcceptHost} localhost

{eCM}#SSH-connect from any machine within saigon office{eEC}
keyUrl="{sshKeyUrl}" ; keyFile=$(mktemp) ; wget -O $keyFile -q $keyUrl #download key from S3
ssh -p {sshPort} -i $keyFile {autoAcceptHost} {ENUJ_PHYSICAL_IP}
'
'''.format(
  CM=CM, EC=EC,  eCM=eCM, eEC=eEC,
  sshPort=sshPort,
  sshKeyFile=sshKeyFile,
  sshKeyUrl=sshKeyUrl,
  ENUJ_PHYSICAL_IP=ENUJ_PHYSICAL_IP,
  autoAcceptHost='-o "StrictHostKeyChecking no"',
)


def step_printSSHSyntax(containerName):
  sshKeyFile, sshPort = getSshKeyPort(containerName)
  sshKeyUrl = getSshKeyURL(containerName)
  assert True \
         and sshKeyFile is not None \
         and sshPort is not None \
         and sshKeyUrl is not None, 'Cannot find ssh key for container name=%s' % containerName

  return '''
echo '
{eCM}#ssh command syntax{eEC}
keyUrl="{sshKeyUrl}" ; keyFile=$(mktemp) ; wget -O $keyFile -q $keyUrl #download key from S3
ssh -p {sshPort} -i $keyFile {autoAcceptHost} {containerUser}@{ENUJ_PHYSICAL_IP}
'
'''.format(
  CM=CM, EC=EC,  eCM=eCM, eEC=eEC,
  sshPort=sshPort,
  sshKeyFile=sshKeyFile,
  sshKeyUrl=sshKeyUrl,
  containerUser=getContainerUser(containerName),
  ENUJ_PHYSICAL_IP=ENUJ_PHYSICAL_IP,
  autoAcceptHost='-o "StrictHostKeyChecking no"',
)


def step_printRSYNCSyntax(containerName):
  containerRsyncPort = getDockerRsyncPort(containerName)
  return '''
echo '
{eCM}#rsync command syntax{eEC}
export ENUJ_RSYNC_FROM={eER}YOUR_LOCAL_PATH{eEC} {eCM}#what to rsync from your local files/folders{eEC}
export ENUJ_RSYNC_TO={eER}YOUR_SUB_PATH_UNDER_REMOTE_HOME{eEC} {eCM}#rsync to sub-folder under remote home {REMOTE_RSYNC_HOME}{eEC}
rsync -chazkP $ENUJ_RSYNC_FROM rsync://{ENUJ_PHYSICAL_IP}:{containerRsyncPort}/volume/$ENUJ_RSYNC_TO {eCM}#do rsync{eEC}
rsync rsync://{ENUJ_PHYSICAL_IP}:{containerRsyncPort}/volume/$ENUJ_RSYNC_TO {eCM}#aftermath check i.e. remote folder listing{eEC}
'
'''.format(
  CM=CM, EC=EC,  eCM=eCM, eEC=eEC, eER=eER,
  ENUJ_PHYSICAL_IP=ENUJ_PHYSICAL_IP,
  containerRsyncPort=containerRsyncPort,
  REMOTE_RSYNC_HOME=getUserHome(containerName),
)


pass
##endregion common info & step


def isValidEnujImage(imageName):
  """Check if imageName is supported by ENUJ CLOUD i.e. defined at class `ENUJ_CLOUD.config.enuj_input.EnujDockerImage` """
  import inspect
  attALL = inspect.getmembers(EnujDockerImage, lambda att: not (inspect.isroutine(att))) #get class attribute ref. https://stackoverflow.com/a/9058322/248616
  supportedImages = [att[1] for att in attALL] #get attribute value by string ref. pycharm debug at `attALL`

  return imageName in supportedImages


##region container user
pass

def getContainerUser(containerName):
  containerImage = DockerUtil.getContainerImage(containerName)
  if not isValidEnujImage(containerImage): return None

  return ContainerUser[containerImage]


def getUserHome(containerName):
  containerImage = DockerUtil.getContainerImage(containerName)
  if not isValidEnujImage(containerImage): return None

  return ContainerUserHome[containerImage]


def getUserHome_fromImageName(imageName):
  if not isValidEnujImage(imageName): return None
  return ContainerUserHome[imageName]


pass
##endregion container user
