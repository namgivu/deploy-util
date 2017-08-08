#!/usr/bin/env python2.7
pass

"""
NOTE:
When console window is too small, the prompt requires us to scroll manually when calling `git log`
Make sure the console is a big enough for the git log
"""

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
Pull code from github repo info
  CODE_GIT_REPO   = {CM}{CODE_GIT_REPO}   {EC}
  CODE_GIT_BRANCH = {CM}{CODE_GIT_BRANCH} {EC}
  PULL_TO         = {CM}{CODE_HOME} {EC}
'''.format(
  HL=HL,CM=CM,EC=EC,

  CODE_GIT_REPO=CODE_GIT_REPO,
  CODE_GIT_BRANCH=CODE_GIT_BRANCH,
  CODE_HOME=CODE_HOME,
)

steps='''
#Pulling code from github... BEGIN

  {HL}#prepare ssh connection{EC}
  eval $(ssh-agent -s) > /dev/null
  ssh-add {REMOTE_GITHUB_KEY} > /dev/null

  
  {HL}#git pull the code {EC}  
  echo ; echo '{eCM}PULL PROGRESS{eEC}'
  git -C {CODE_HOME} checkout . #revert changes made to your working copy ref. http://stackoverflow.com/a/1146981
  git -C {CODE_HOME} fetch #get latest remote
  git -C {CODE_HOME} checkout {CODE_GIT_BRANCH}
  git -C {CODE_HOME} pull

  {HL}#current code status {EC}
  echo ; echo '{eCM}CURRENT COMMIT{eEC}'
  git -C {CODE_HOME} log -n2

  echo ; echo '{eCM}CURRENT BRANCH{eEC}'
  git -C {CODE_HOME} branch

#Pulling code from github... END
'''.format(
  HL=HL,CM=CM,EC=EC,
  eHL=eHL,eCM=eCM,eEC=eEC,

  CODE_HOME=CODE_HOME,
  CODE_GIT_BRANCH=CODE_GIT_BRANCH,
  REMOTE_GITHUB_KEY=REMOTE_GITHUB_KEY,
)

print(infos)
print(steps)
#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun git pulling code'
)
