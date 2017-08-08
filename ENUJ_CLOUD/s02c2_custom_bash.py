#!/usr/bin/env python2.7
pass

#load config package
from config import *

##region parse params

options = dict(
  shortOpts='a:c:u:',
  longOpts=['autorun=', 'container', 'containerUser'],
)

isAutorun = getArg('-a', options)
CONTAINER_NAME_or_ID = getArg('-c', options)

assert CONTAINER_NAME_or_ID is not None, '-c param is required i.e. CONTAINER_NAME_or_ID'
CONTAINER_NAME = DockerUtil.getNameOrFail(CONTAINER_NAME_or_ID)

##endregion parse params


#region print infos & steps

infos = '''
Make the prompt in color for container {CONTAINER_NAME}
'''.format(
  CM=CM, EC=EC,
  CONTAINER_NAME=CONTAINER_NAME,
)

#bashrc entry to make prompt in color
#TODO Why we have to source .bashrc every time we ssh to it?
CUSTOM_BASH=r"""
#prompt color
PS1='\n${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@%s\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\n\$ '

#ls with color
export LS_OPTIONS='--color=auto'
alias ls='ls $LS_OPTIONS'
""" % CONTAINER_NAME #keep string as-is ie. no-escape ref. https://stackoverflow.com/a/4703526/248616

#write CUSTOM_BASH to temp file
import tempfile
fileCUSTOM_BASH = tempfile.NamedTemporaryFile().name #get a temp filename ref. https://stackoverflow.com/a/39984066/248616
with open(fileCUSTOM_BASH, "w") as f: f.write(CUSTOM_BASH + '\n') #write string to file ref. https://stackoverflow.com/a/5214587/248616

#the CUSTOM_BASH file name on remote side
remote_fileCUSTOM_BASH_underHome = 'prompt_color.%s' % randomTag()

#expand remote bashrc and clean up
remoteCmd = '''
sudo touch ~/.bashrc
sudo chown -R {CONTAINER_USER}:{CONTAINER_USER} ~/.bashrc 
cat ~/{remote_fileCUSTOM_BASH_underHome} >> ~/.bashrc
sudo rm -f ~/{remote_fileCUSTOM_BASH_underHome}
'''.format(
  remote_fileCUSTOM_BASH_underHome=remote_fileCUSTOM_BASH_underHome,
  CONTAINER_USER=getContainerUser(CONTAINER_NAME),
).strip().replace('\n',' ; ')


steps = '''
{CM}#upload 'CUSTOM_BASH' file {EC}
{ENUJ_CLOUD_HOME}/s02b_rsync_util.py -c {CONTAINER_NAME} -f {fileCUSTOM_BASH} -t {remote_filePS1} -a 1

{CM}#remote run to expand bashrc with 'fileCUSTOM_BASH' {EC}
{ENUJ_CLOUD_HOME}/s02a_ssh_connect.py -c {CONTAINER_NAME} -r "{remoteCmd}" -a 1

{CM}#aftermath{EC}
echo '
Remote prompt with color updated.
You may need to refresh your command prompt e.g.
{eCM}source ~/.bashrc{eEC}
'

'''.format(
  CM=CM, EC=EC,  eCM=eCM, eEC=eEC,

  fileCUSTOM_BASH=fileCUSTOM_BASH,
  remote_filePS1=remote_fileCUSTOM_BASH_underHome,

  ENUJ_CLOUD_HOME=ENUJ_CLOUD_HOME,
  CONTAINER_NAME=CONTAINER_NAME,
  remoteCmd=remoteCmd,
)


print(infos)

if not isAutorun:  #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
