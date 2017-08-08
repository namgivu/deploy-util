#!/usr/bin/env python2.7

#region common input entries
import os

SCRIPT_HOME   = os.path.abspath(os.path.dirname(__file__))
UTILITY_ROOT  = os.path.abspath('%s/../..' % SCRIPT_HOME)

USER_HOME   = os.environ['HOME'] #TODO consider to replace this by expanduser('~') ie. get user home folder @ all platform ref. http://stackoverflow.com/a/4028943/248616
BASHRC      = '%s/.bashrc' % USER_HOME

REMOTE_HOME       = '$HOME'
REMOTE_SSH_HOME   = '$HOME/.ssh'
REMOTE_HOME_bash  = REMOTE_HOME.replace('$', '\\$')


DEPLOY_HOME   = SCRIPT_HOME
CODE_HOME     = '%s/code' % UTILITY_ROOT
DEPLOY_CONFIG = '%s/deploy_flask/config' % UTILITY_ROOT

BASH_UTIL   = '%s/util/bash_util' % UTILITY_ROOT
PYTHON_UTIL = '%s/util/python_util' % UTILITY_ROOT

PIP_UTIL                = '%s/deploy_flask/pip_package' % UTILITY_ROOT
PIP_REQUIREMENT_DEFAULT = '%s/requirements.txt' % CODE_HOME

REMOTE_SSL_HOME = '/etc/apache2/ssl'

UTIL_PRUNED_LIST = None #list of pruned file/folder; separated by colon : e.g. 'deploy_brain:deploy_mysql' or left empty to remove nothing
#endregion common input entries


#region load python utility
import sys

#load python path entry
sys.path.append(UTILITY_ROOT)

#load python util
from util.python_util import *

#endregion load python utility
