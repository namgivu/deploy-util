#!/usr/bin/env python2.7
pass

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options)
#endregion parse params


#region print infos & steps
infos='''
#Clone code from github repo info
  CODE_GIT_REPO   = {CM}{CODE_GIT_REPO}   {EC}
  CODE_GIT_BRANCH = {CM}{CODE_GIT_BRANCH} {EC}
  CLONE_TO        = {CM}{CODE_HOME}        {EC}
'''.format(
  HL=HL,CM=CM,EC=EC,
  CODE_GIT_REPO=CODE_GIT_REPO,
  CODE_GIT_BRANCH=CODE_GIT_BRANCH,
  CODE_HOME=CODE_HOME,
)


steps='''
#Cloning code from github... BEGIN

  {HL}#prepare folder {EC}
  rm -rf {CODE_HOME}; mkdir -p {CODE_HOME}

  {HL}#do git clone {EC}
  {CM}#use specific ssh key ref. http://stackoverflow.com/a/4565746/248616 {EC}
  ssh-agent bash -c "ssh-add {REMOTE_GITHUB_KEY}; git clone {CODE_GIT_REPO} -b {CODE_GIT_BRANCH} {CODE_HOME}"


  {HL}#aftermath check {EC}
  echo; echo '{eCM}CODE_HOME:{eEC}'
  ls -la {CODE_HOME}

#Cloning code from github... END
'''.format(
  HL=HL,CM=CM,EC=EC,
  eCM=eCM,eEC=eEC,

  CODE_HOME=CODE_HOME,
  CODE_GIT_REPO=CODE_GIT_REPO,
  CODE_GIT_BRANCH=CODE_GIT_BRANCH,
  REMOTE_GITHUB_KEY=REMOTE_GITHUB_KEY,
)

print(infos)

if not isAutorun:
  print(steps)
#endregion print infos & steps


#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
