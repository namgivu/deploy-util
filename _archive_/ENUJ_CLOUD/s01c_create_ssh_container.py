#!/usr/bin/env python2.7
pass

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:p:c:',
  longOpts  = ['autorun=', 'port=', 'container'],
)

isAutorun = getArg('-a', options)

#TODO ssh port to be selected automatically as 22xx ref. https://stackoverflow.com/q/44940239/248616
CONTAINER_SSH_PORT = getArg('-p', options)
CONTAINER_NAME_or_ID = getArg('-c', options)

if not CONTAINER_NAME_or_ID:  raise Exception('-c param is required i.e. CONTAINER_NAME_or_ID')
if not CONTAINER_SSH_PORT:    raise Exception('-p param is required i.e. CONTAINER_SSH_PORT')
#endregion parse params


#infer CONTAINER_NAME from CONTAINER_NAME_or_ID
CONTAINER_NAME = DockerUtil.getNameOrFail(CONTAINER_NAME_or_ID)


#region print infos & steps

DOCKERSSH_NAME_LOWERCASE = 'docker-ssh_%s_%s' % (CONTAINER_SSH_PORT, CONTAINER_NAME) #force to use container name i.e. if IP is given, parse the name from it
SSH_KEY_FILE='%s/%s' % (ENUJ_SSH_KEY_VAULT, DOCKERSSH_NAME_LOWERCASE)
SSH_KEY_FILE_pub='%s.pub' % SSH_KEY_FILE
AUTHORIZED_KEYS_FILE='%s.authorized_keys' % SSH_KEY_FILE

SSH_KEY_FILE_PUBLISHED='{ENUJ_SSH_KEY_PUBLISHED_VAULT}/{DOCKERSSH_NAME_LOWERCASE}_{randomSuffix}'.format(
  ENUJ_SSH_KEY_PUBLISHED_VAULT=ENUJ_SSH_KEY_PUBLISHED_VAULT,
  DOCKERSSH_NAME_LOWERCASE=DOCKERSSH_NAME_LOWERCASE,
  randomSuffix=randomTag()
)


infos = '''
Create SSH connect to a Docker container via jeroenpeeters/docker-ssh ref. https://github.com/jeroenpeeters/docker-ssh#docker-ssh--
      parent container name : {CM}{CONTAINER_NAME}{EC}
  docker-ssh container name : {CM}{DOCKERSSH_NAME_LOWERCASE}{EC}
              ssh key vault : {CM}{ENUJ_SSH_KEY_VAULT}{EC}
'''.format(
  CM=CM, EC=EC,
  CONTAINER_NAME=CONTAINER_NAME,
  DOCKERSSH_NAME_LOWERCASE=DOCKERSSH_NAME_LOWERCASE,
  ENUJ_SSH_KEY_VAULT=ENUJ_SSH_KEY_VAULT,
)

steps='''
{CM}#generate ssh key ref. https://stackoverflow.com/a/27504514/248616{EC} #auto say yes ref. https://stackoverflow.com/a/15890748/248616
echo -e  'y\\n' | ssh-keygen -q -t rsa -N '' -f {SSH_KEY_FILE} 1>/dev/null #quiet type new-pass-phrase file

{CM}#extract public key ref. https://askubuntu.com/a/53555/22308{EC}
ssh-keygen -y -f {SSH_KEY_FILE} > {SSH_KEY_FILE_pub} # -y for public-key 

{CM}#make authorized_keys file{EC}
cat {SSH_KEY_FILE_pub} > {AUTHORIZED_KEYS_FILE}

{CM}#publish key so that we can ssh from anywhere using key url{EC}
sudo mkdir -p {ENUJ_SSH_KEY_PUBLISHED_VAULT} #create published vault folder
sudo touch {ENUJ_SSH_KEY_PUBLISHED_VAULT}/index.html #disable folder listing
sudo cp -f {SSH_KEY_FILE} {SSH_KEY_FILE_PUBLISHED} #copy ssh key into published folder
sudo chmod 644 {SSH_KEY_FILE_PUBLISHED} #set permission to download/read


{CM}#aftermath key creation{EC}
echo
echo 'Created key files'
ls -l {ENUJ_SSH_KEY_VAULT}/{DOCKERSSH_NAME_LOWERCASE}*

{CM}#start docker-ssh container to have ssh util for the targeted container{EC}
echo
docker run -d -p {CONTAINER_SSH_PORT}:22 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v {AUTHORIZED_KEYS_FILE}:/authorized_keys \
  -e CONTAINER={CONTAINER_NAME_or_ID} -e AUTH_MECHANISM=publicKey \
  -e AUTHORIZED_KEYS=/authorized_keys \
  --name {DOCKERSSH_NAME_LOWERCASE} \
  jeroenpeeters/docker-ssh

{CM}#aftermath check{EC}
echo
docker ps -f name=^/{DOCKERSSH_NAME_LOWERCASE} #this should print nothing 
'''.format(
  CM=CM, EC=EC,  eCM=eCM, eEC=eEC,
  SSH_KEY_FILE=SSH_KEY_FILE,
  SSH_KEY_FILE_pub=SSH_KEY_FILE_pub,
  DOCKERSSH_NAME_LOWERCASE=DOCKERSSH_NAME_LOWERCASE,
  CONTAINER_NAME_or_ID=CONTAINER_NAME_or_ID,
  AUTHORIZED_KEYS_FILE=AUTHORIZED_KEYS_FILE,
  ENUJ_SSH_KEY_VAULT=ENUJ_SSH_KEY_VAULT,
  ENUJ_PHYSICAL_IP=ENUJ_PHYSICAL_IP,
  CONTAINER_SSH_PORT=CONTAINER_SSH_PORT,
  ENUJ_SSH_KEY_PUBLISHED_VAULT=ENUJ_SSH_KEY_PUBLISHED_VAULT,
  SSH_KEY_FILE_PUBLISHED=SSH_KEY_FILE_PUBLISHED,
)


import ntpath
filename=ntpath.basename(SSH_KEY_FILE_PUBLISHED)
SSH_KEY_URL = makeEnujKeyUrl(filename)


steps += '''
%s
''' % step_printSshConnectGuide(SSH_KEY_FILE, CONTAINER_SSH_PORT, SSH_KEY_URL)


print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
