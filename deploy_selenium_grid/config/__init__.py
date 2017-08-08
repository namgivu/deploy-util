##region register python-path entry
pass

#script home
import os
SCRIPT_HOME = os.path.abspath(os.path.dirname(__file__))

#basic path
UTILITY_ROOT              = os.path.abspath('%s/../..' % SCRIPT_HOME)
DEPLOY_SELENIUM_GRID_HOME = '%s/deploy_selenium_grid' % UTILITY_ROOT
DOCKER_BASH_UTIL          = os.path.abspath('%s/util/bash_util/docker_util' % UTILITY_ROOT)

#add python path entry
import sys
sys.path.append(UTILITY_ROOT)

pass
##endregion register python-path entry


"""The common python util MUST be declared here; NOT in any other sub-module"""
#load common python config
from util.python_util import *


from deploy_common.config import *