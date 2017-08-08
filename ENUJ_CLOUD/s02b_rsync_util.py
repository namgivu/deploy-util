#!/usr/bin/env python2.7
pass

#load config package
from config import *

##region parse params

options = dict(
  shortOpts='a:c:f:t:p:',
  longOpts=['autorun=', 'container=', 'from=', 'to=', 'pruneList='],
)

isAutorun = getArg('-a', options)
CONTAINER_NAME_or_ID = getArg('-c', options)

ENUJ_RSYNC_FROM  = getArg('-f', options)
ENUJ_RSYNC_TO    = getArg('-t', options)
ENUJ_RSYNC_PRUNE = getArg('-p', options) #the list of pruned files/folders in formation file01:folder02:...; at top level of the rsynced folder only

if not CONTAINER_NAME_or_ID: raise Exception('-c param is required i.e. CONTAINER_NAME_or_ID')
if not ENUJ_RSYNC_FROM:  raise Exception('-f param is required i.e. ENUJ_RSYNC_FROM')
if not ENUJ_RSYNC_TO:    raise Exception('-t param is required i.e. ENUJ_RSYNC_TO')

##endregion parse params

ENUJ_RSYNC_FROM = ENUJ_RSYNC_FROM.replace('//','/')
rsyncedFolder = ENUJ_RSYNC_FROM

#always work with name not the id
CONTAINER_NAME = DockerUtil.getNameOrFail(CONTAINER_NAME_or_ID)

#get docker-rsync port
CONTAINER_RSYNC_PORT = getDockerRsyncPort(CONTAINER_NAME)
assert CONTAINER_RSYNC_PORT is not None

#prune prepare
removeeList = ENUJ_RSYNC_PRUNE
if removeeList:
  #clone ENUJ_RSYNC_FROM to temp folder to prune it
  import tempfile ; rsyncedFolder = tempfile.mkdtemp() #create temp folder ref. https://stackoverflow.com/a/3223615/248616
  rsyncedFolder += '/cloneENUJ_RSYNC_FROM'+'/' #the ending '/' is to serve rsync
  import shutil ; shutil.copytree(src=ENUJ_RSYNC_FROM, dst=rsyncedFolder) #copy folder ref. https://stackoverflow.com/a/1994840/248616

  #do pruning via rm command
  removeeList = removeeList.split(':')
  for removee in removeeList:
    shutil.rmtree('{rsyncedFolder}/{removee}'.format(
      rsyncedFolder=rsyncedFolder,
      removee=removee.strip(),
    ))
  cleanupFolder = rsyncedFolder

#region print infos & steps

print removeeList

infos = '''
Rsync local folder to a Docker container via its name
  container name : {CM}{CONTAINER_NAME}{EC}
      FROM local : {CM}{ENUJ_RSYNC_FROM}{EC}
       TO remote : {CONTAINER_NAME}@{CM}{REMOTE_RSYNCED_FOLDER}{EC}
{pruneInfo}        
'''.format(
  CM=CM, EC=EC,
  CONTAINER_NAME=CONTAINER_NAME,
  ENUJ_RSYNC_FROM=ENUJ_RSYNC_FROM,
  REMOTE_RSYNCED_FOLDER='{REMOTE_RSYNC_HOME}/{ENUJ_RSYNC_TO}'.format(
    REMOTE_RSYNC_HOME=getUserHome(CONTAINER_NAME),
    ENUJ_RSYNC_TO=ENUJ_RSYNC_TO,
  ),
  pruneInfo='''
      prune list : {removeeList}
 local pruned at : {rsyncedFolder} 
  '''.format(
    removeeList=removeeList,
    rsyncedFolder=rsyncedFolder,
  ) if removeeList else ''
)


steps = '''
{CM}#do rsync{EC}
rsync -chazkP {rsyncedFolder} rsync://{ENUJ_PHYSICAL_IP}:{CONTAINER_RSYNC_PORT}/volume/{ENUJ_RSYNC_TO}

{CM}#aftermath check by listing remote folder{EC}
echo
echo 'Remote content after rsynced'
rsync rsync://{ENUJ_PHYSICAL_IP}:{CONTAINER_RSYNC_PORT}/volume/{ENUJ_RSYNC_TO}
'''.format(
  CM=CM, EC=EC,
  rsyncedFolder=rsyncedFolder,
  ENUJ_RSYNC_TO=ENUJ_RSYNC_TO,
  ENUJ_PHYSICAL_IP=ENUJ_PHYSICAL_IP,
  CONTAINER_RSYNC_PORT=CONTAINER_RSYNC_PORT,
)

print(infos)

if not isAutorun:  #print steps only when not autorun
  print(steps)

#endregion print infos & steps


if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)


#clean up
if cleanupFolder: shutil.rmtree(cleanupFolder)
