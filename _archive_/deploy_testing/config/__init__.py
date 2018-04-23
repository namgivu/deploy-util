##region register python-path entry
pass

#script home
import os
SCRIPT_HOME = os.path.abspath(os.path.dirname(__file__))

#basic path
UTILITY_ROOT = os.path.abspath('%s/../..' % SCRIPT_HOME)
DEPLOY_TESTING_HOME = '%s/deploy_testing' % UTILITY_ROOT

#add python path entry
import sys
sys.path.append(UTILITY_ROOT)

pass
##endregion register python-path entry


"""The common python util MUST be declared here; NOT in any other sub-module"""
#load common python config
from util.python_util import *


from deploy_common.config import *