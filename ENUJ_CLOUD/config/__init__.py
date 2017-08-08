#!/usr/bin/env python2.7
pass


##region base path

#script home
import os
cSCRIPT_HOME = os.path.abspath(os.path.dirname(__file__))

#util root
UTILITY_ROOT = os.path.abspath('%s/../..' % cSCRIPT_HOME)

##endregion base path


#python-path entry
import sys
sys.path.append(UTILITY_ROOT)


#load common python config
from util.python_util import *


#load config files
from enuj_input import *
from ENUJ_CLOUD.common import *
