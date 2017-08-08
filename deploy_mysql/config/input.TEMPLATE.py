#!/usr/bin/env python2.7

from common import *

DB_HOST           = 'YOUR_DB_HOST' #TODO support ip2nd@ip besides localhost@ip ie. when dumpdb for `rbs PROD` from `brain EC2`
DB_USER           = 'YOUR_DB_USER'
DB_PASS           = 'YOUR_DB_PASS'
DB_NAME           = 'YOUR_DB_NAME'

MYSQL_DEBUG       = False #True/False = yes/no to print execution progress

#TODO Move this entry to `input_initdb.py`
SCRIPT_FILE       = '' #left empty so that to use latest backup on S3
SCRIPT_FILE       = '/path/to/YOUR_SCRIPT_FILE/file' #use script at this local path
