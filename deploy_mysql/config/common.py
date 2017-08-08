#!/usr/bin/env python2.7

import os
SCRIPT_HOME       = os.path.abspath(os.path.dirname(__file__))
UTILITY_ROOT      = os.path.abspath('%s/../..' % SCRIPT_HOME)

S3_KEY            = 'YOUR_S3_KEY'
S3_SECRET         = 'YOUR_S3_SECRET'

S3_BUCKET         = 'YOUR_S3_BUCKET'
DB_LATEST_BACKUP  = '%s/backup.sql' % S3_BUCKET
DB_NAME_DEFAULT   = 'YOUR_DB_NAME'

DEPLOY_CONFIG     = '%s/deploy_mysql/config' % UTILITY_ROOT

DB_CONN           = '%s/mysql-connection' % DEPLOY_CONFIG #db connection file
DB_CONN_TEMPLATE  = '%s/mysql-connection.TEMPLATE' % DEPLOY_CONFIG #db connection file


#region load python utility
import sys

#load python path entry
sys.path.append(UTILITY_ROOT)

#load python util
from util.python_util import *

#endregion load python utility
