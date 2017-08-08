#!/usr/bin/env python2.7

pass
#TODO Add option to mute output
#TODO use deploy_common util
pass

from common import * #initiate common asset
from input  import * #load the inputs


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
REMOTE_UTIL_PATH = '{REMOTE_HOME}/deploy.{DEPLOY_ID}'.format(
  REMOTE_HOME=REMOTE_HOME_bash,
  DEPLOY_ID=DEPLOY_ID,
)

#remote 's github ssh key folder
REMOTE_GITHUB_PATH = '%s/.ssh/' % REMOTE_HOME_bash

##endregion local vs remote mapping


##region loading github ssh key

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

##endregion loading github ssh key


#region print infos & steps
infos='''
{HL}We are uploading below assets to remote host{EC}
  THE_GITHUB : from {CM}{printedCODE_GITHUB_KEY} {EC}
                 to {CM}remote @ {REMOTE_GITHUB_PATH}{EC}

  THE_UTIL   : from {CM}{THE_UTIL}{EC}
                 to {CM}remote @ {REMOTE_UTIL_PATH}{EC}
'''.format(
  HL=HL,CM=CM,EC=EC,

  THE_UTIL=THE_UTIL,
  printedCODE_GITHUB_KEY=CODE_GITHUB_KEY if CODE_GITHUB_KEY else CODE_GITHUB_KEY_URL,
  REMOTE_UTIL_PATH=REMOTE_UTIL_PATH  .replace(REMOTE_HOME_bash, REMOTE_HOME),
  REMOTE_GITHUB_PATH=REMOTE_GITHUB_PATH.replace(REMOTE_HOME_bash, REMOTE_HOME),
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
  remoteRun='%s/00_ssh_connect.py' % DEPLOY_HOME,
  cmds=cmds,
)
#endregion prepare aftermath command


steps='''
#Uploading assets to remote host... BEGIN

  {HL}#clone THE_UTIL to temp folder {EC}
  rm -rf {tempDir} ; rsync -chazk {THE_UTIL}/ {tempDir}/

  {HL}#prune THE_UTIL at temp {EC}
  find {tempDir} -type f -name '*.pyc' -delete #delete all *.pyc ref. http://unix.stackexchange.com/a/116390/17671
  rm -rf {tempDir}/.git*
  rm -rf {tempDir}/.idea
  rm -rf {tempDir}/88_YOUR_STEP.py
  rm -rf {tempDir}/_daily_
  {prunedList}

  {HL}#do upload THE_GITHUB {EC}
  export githubKey={githubKey} {downloadedNote}
  {upload} -s $githubKey -t {REMOTE_GITHUB_PATH} -c 'THE_GITHUB'

  {HL}#do upload THE_UTIL; please mind the ending slash '/' {EC}
  {upload} -s {THE_UTIL_pruned}/ -t {REMOTE_UTIL_PATH}/ -c 'THE_UTIL'

  {HL}#clean up {EC}
  rm -rf {tempDir}

  {HL}#aftermath checking {EC}
  {shAftermath}

#Uploading assets to remote host... END
'''.format(
  HL=HL,CM=CM,EC=EC,

  upload='%s/01_upload_file.py' % DEPLOY_HOME,

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
print(steps)
#endregion print infos & steps


#run it
if isAutorun: runPrintedSteps(
  steps, headline='Autorun util&github uploading'
)
