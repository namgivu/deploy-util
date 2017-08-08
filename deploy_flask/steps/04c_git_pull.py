#!/usr/bin/env python2.7
pass

"""
For some reason the prompt requires our input when run this git pull util
SOLUTION: Make sure directly call git pull on remote host succeeding first
"""

from common   import * #initiate common asset
from input    import * #load the inputs

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
  PULL_TO         = {CM}{APP_CODE} {EC}
'''.format(
  HL=HL,CM=CM,EC=EC,

  CODE_GIT_REPO=CODE_GIT_REPO,
  CODE_GIT_BRANCH=CODE_GIT_BRANCH,
  APP_CODE=APP_CODE,
)

steps='''
#Pulling code from github... BEGIN

  {HL}#prepare ssh connection{EC}
  eval $(ssh-agent -s) > /dev/null
  ssh-add {REMOTE_GITHUB_KEY} > /dev/null

  
  {HL}#git pull the code {EC}  
  echo ; echo '{eCM}PULL PROGRESS{eEC}'
  git -C {APP_CODE} checkout . #revert changes made to your working copy ref. http://stackoverflow.com/a/1146981
  git -C {APP_CODE} fetch #get latest remote
  git -C {APP_CODE} checkout {CODE_GIT_BRANCH}
  git -C {APP_CODE} pull

  {HL}#current code status {EC}
  echo ; echo '{eCM}CURRENT COMMIT{eEC}'
  git -C {APP_CODE} log -n2

  echo ; echo '{eCM}CURRENT BRANCH{eEC}'
  git -C {APP_CODE} branch

#Pulling code from github... END
'''.format(
  HL=HL,CM=CM,EC=EC,
  eHL=eHL,eCM=eCM,eEC=eEC,

  APP_CODE=APP_CODE,
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
