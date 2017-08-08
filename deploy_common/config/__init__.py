#!/usr/bin/env python2.7
pass

##region base path

#script home
import os
SCRIPT_HOME = os.path.abspath(os.path.dirname(__file__))

#add python path entry
UTILITY_ROOT = os.path.abspath('%s/../..' % SCRIPT_HOME)

#deploy common util home
DEPLOY_COMMON_HOME = os.path.abspath('%s/deploy_common' % UTILITY_ROOT)

##endregion base path


#register python-path entry
import sys
sys.path.append(UTILITY_ROOT)

#load common python config
from util.python_util import *

#entries from `input 0th`
from common_input import *
from common_input_0th import *


##region common input entries
USER_HOME   = os.environ['HOME'] #TODO consider to replace this by expanduser('~') ie. get user home folder @ all platform ref. http://stackoverflow.com/a/4028943/248616
BASHRC      = '%s/.bashrc' % USER_HOME

REMOTE_HOME       = '$HOME'
REMOTE_SSH_HOME   = '$HOME/.ssh'
REMOTE_HOME_bash  = REMOTE_HOME.replace('$', '\\$')


CODE_HOME     = '%s/code' % UTILITY_ROOT
BASH_UTIL   = '%s/util/bash_util' % UTILITY_ROOT
PYTHON_UTIL = '%s/util/python_util' % UTILITY_ROOT

"""referring-input = input entries that were inferred from `common input 0th` """
if not DEPLOY_ID:
  DEPLOY_ID = '%s.%s' % (APP_NAME, DEPLOY_TARGET)


#when github key is provided via url, we name it as follow
DOWNLOAD_GITHUB_KEY = makeGithubKeyFilename(DEPLOY_ID)

#region extract github ssh related section
"""These be used to write into file ~/.ssh/config to tell git command to use our specific github key"""
if CODE_GIT_REPO:
  splits00 = CODE_GIT_REPO.split(':')
  if len(splits00)>0 :
    splits22 = splits00[0].split('@')
    if len(splits22)>0 :
      CODE_GIT_REPO_USER = splits22[0]
      CODE_GIT_REPO_HOST = splits22[1]
#endregion extract github ssh related section


#remote 's github ssh key
REMOTE_GITHUB_KEY  = getRemoteGithubKey(REMOTE_SSH_HOME, DEPLOY_ID)

##endregion common input entries


#region validate input
if not CODE_GITHUB_KEY and not CODE_GITHUB_KEY_URL:
  raise Exception('Either CODE_GITHUB_KEY or CODE_GITHUB_KEY_URL is required')

if not HOST_SSH_KEY and not HOST_SSH_KEY_URL:
  raise Exception('Either HOST_SSH_KEY or HOST_SSH_KEY_URL is required')

if not DEPLOY_HOME_PREFIX: DEPLOY_HOME_PREFIX='deploy'

pass
#endregion validate input


#region info printing
FLASK_DEPLOY_INFO = '''
{HL}#Flask app deploy config {EC}
       APP_NAME: {APP_NAME}
  DEPLOY_TARGET: {DEPLOY_TARGET}
      DEPLOY_ID: {CM}{DEPLOY_ID}{EC}
'''.format(
  HL=HL,CM=CM,EC=EC,ER=ER,

  APP_NAME=APP_NAME,
  DEPLOY_TARGET=DEPLOY_TARGET,
  DEPLOY_ID=DEPLOY_ID,
)
#endregion info printing