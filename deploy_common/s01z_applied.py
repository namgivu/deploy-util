#!/usr/bin/env python2.7

pass
#TODO Add option to mute output
#TODO Extract github key into its own separated step
pass

#load config package
from config import *


#region load params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun   = getArg('-a', options)
prunedList  = UTIL_PRUNED_LIST #list of pruned file/folder; separated by colon : e.g. 'deploy_brain:deploy_mysql' or left empty to remove nothing
#endregion load params


#region input validate
if not prunedList:
  prunedList='' #TODO put in some default item in prunedList
#endregion input validate


##region local vs remote mapping

#local 's utility folder
THE_UTIL = UTILITY_ROOT

#remote 's utility folder
if HOST_DOCKERRSYNC_URL: #host is under docker-rsync mode
  REMOTE_UTIL_PATH = '{DEPLOY_HOME_PREFIX}.{DEPLOY_ID}'.format(
    DEPLOY_HOME_PREFIX=DEPLOY_HOME_PREFIX,
    DEPLOY_ID=DEPLOY_ID,
  )
else: #non-docker host
  REMOTE_UTIL_PATH = '{REMOTE_HOME}/{DEPLOY_HOME_PREFIX}.{DEPLOY_ID}'.format(
    DEPLOY_HOME_PREFIX=DEPLOY_HOME_PREFIX,
    REMOTE_HOME=REMOTE_HOME_bash,
    DEPLOY_ID=DEPLOY_ID,
  )

#remote 's github ssh key folder
if HOST_DOCKERRSYNC_URL: #host is under docker-rsync mode
  REMOTE_GITHUB_PATH = '.ssh'
else: #non-docker host
  REMOTE_GITHUB_PATH = '%s/.ssh' % REMOTE_HOME_bash

##endregion local vs remote mapping


##region the upload util
if HOST_DOCKERRSYNC_URL: #host is under docker-rsync mode
  uploadUtil = '%s/s01b_docker_rsync.py' % DEPLOY_COMMON_HOME
else: #non-docker host
  uploadUtil = '%s/s01_rsync_file.py' % DEPLOY_COMMON_HOME
##endregion the upload util


##region loading github ssh key
import sys ; sys.stdout.write('Checking github SSH key... ') ; sys.stdout.flush() #print without newline ref. https://stackoverflow.com/a/493399/248616

#default taking the local key first
githubKey = CODE_GITHUB_KEY
keyFilename = makeGithubKeyFilename(DEPLOY_ID)

if CODE_GITHUB_KEY:
  from tempfile import mktemp
  githubKey = mktemp()

  import shutil
  shutil.copy2(CODE_GITHUB_KEY, githubKey) #copy file ref. http://stackoverflow.com/a/123238/248616

  githubKey = renameFile(githubKey, keyFilename)

if not CODE_GITHUB_KEY:
  #download key from shared url when local key not provided
  githubKey = downloadFile(url=CODE_GITHUB_KEY_URL, chmod='600')

  #rename key file filename
  githubKey = renameFile(githubKey, keyFilename)

print('DONE')
##endregion loading github ssh key


#region print infos & steps
infos='''
We are uploading below assets to remote host

  THE_GITHUB : from {CM}{printedCODE_GITHUB_KEY} {EC}
                 to {CM}remote @ $HOME/{REMOTE_GITHUB_PATH}{EC}

  THE_UTIL   : from {CM}{THE_UTIL}{EC}
                 to {CM}remote @ $HOME/{REMOTE_UTIL_PATH}{EC}
                 
  uploadUtil : {CM}{uploadUtil}{EC}
'''.format(
  HL=HL,CM=CM,EC=EC,

  THE_UTIL=THE_UTIL,
  printedCODE_GITHUB_KEY=CODE_GITHUB_KEY if CODE_GITHUB_KEY else CODE_GITHUB_KEY_URL,
  REMOTE_UTIL_PATH=REMOTE_UTIL_PATH  .replace(REMOTE_HOME_bash, REMOTE_HOME),
  REMOTE_GITHUB_PATH=REMOTE_GITHUB_PATH.replace(REMOTE_HOME_bash, REMOTE_HOME),

  uploadUtil=uploadUtil,
)


#prepare temp folder to clone THE_UTIL into it
import tempfile ; tempDir = tempfile.mkdtemp()


#region make rm commands from prunedList
rmCmds = []
for p in prunedList.split(':'):
  #skip empty ones
  p = p.strip()
  if not p: continue

  #record rm cmd
  rmCmds.append('rm -rf {tempDir}/{p}'.format(tempDir=tempDir, p=p))
#endregion make rm commands from prunedList


#region prepare aftermath command
cmds='''
  echo '';
  echo -e '{eCM}REMOTE_HOME{eEC}';        ls -l {REMOTE_HOME}; echo '';
  echo -e '{eCM}REMOTE_GITHUB_PATH{eEC}'; ls -l {REMOTE_GITHUB_PATH}; echo '';
  echo -e '{eCM}REMOTE_UTIL_PATH{eEC}';   ls -l {REMOTE_UTIL_PATH}; echo '';
'''.strip().replace('\n','')\
   .format(
  eCM=eCM, eEC=eEC,

         REMOTE_HOME = '\\\\'+REMOTE_HOME_bash,   #the '\\\\' is to get $HOME not-transfer to value when still in locall
  REMOTE_GITHUB_PATH = '\\\\'+REMOTE_GITHUB_PATH, #the '\\\\' noted as above
    REMOTE_UTIL_PATH = '\\\\'+REMOTE_UTIL_PATH,   #the '\\\\' noted as above
)

shAftermath='{remoteRun} --command="{cmds}" --verbose=0 -a 1 '.format(
  remoteRun='%s/s00_ssh_connect.py' % DEPLOY_COMMON_HOME,
  cmds=cmds,
)
#endregion prepare aftermath command


steps= '''
{HL}#Uploading assets to remote host... BEGIN{EC}

  {CM}#clone THE_UTIL to temp folder {EC}
  rm -rf {tempDir} ; rsync -chazk {THE_UTIL}/ {tempDir}/

  {CM}#prune THE_UTIL at temp {EC}
  find {tempDir} -type f -name '*.pyc' -delete #delete all *.pyc ref. http://unix.stackexchange.com/a/116390/17671
  rm -rf {tempDir}/.git*
  rm -rf {tempDir}/.idea
  rm -rf {tempDir}/88_YOUR_STEP.py
  rm -rf {tempDir}/_sandbox_.py
  rm -rf {tempDir}/_daily_
  {prunedList}

  {CM}#do upload THE_GITHUB {EC}
  githubKey={githubKey} {downloadedNote}
  {uploadUtil} -s $githubKey -t {REMOTE_GITHUB_PATH} -c 'THE_GITHUB'

  {CM}#do upload THE_UTIL; please mind the ending slash '/' {EC}
  {uploadUtil} -s {THE_UTIL_pruned}/ -t {REMOTE_UTIL_PATH} -c 'THE_UTIL'

  {CM}#clean up {EC}
  rm -rf {tempDir}

  {CM}#aftermath checking {EC}
  {shAftermath}

{HL}#Uploading assets to remote host... END{EC}
'''.format(
  HL=HL,CM=CM,EC=EC,

  uploadUtil=uploadUtil,

  tempDir=tempDir,
  THE_UTIL=THE_UTIL,
  THE_UTIL_pruned=tempDir,
  githubKey=githubKey,
  downloadedNote='#github key downloaded to this temp file' if githubKey != CODE_GITHUB_KEY else '',
  REMOTE_UTIL_PATH=REMOTE_UTIL_PATH,
  REMOTE_GITHUB_PATH=REMOTE_GITHUB_PATH,

  shAftermath=shAftermath,
  prunedList=''.join(['%s\n  ' % rmCmd  for rmCmd in rmCmds]),
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps


#run it
if isAutorun: runPrintedSteps(
  steps, headline='Autorun rsync util via %s' % os.path.basename(__file__)
)
