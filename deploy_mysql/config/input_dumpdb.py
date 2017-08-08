#!/usr/bin/env python2.7
from .common  import *
from .input   import *
from .initial import *

#region input entries
if not DUMP_FOLDER: DUMP_FOLDER = DB_NAME
DUMP_HOME='$HOME/Desktop/{DUMP_FOLDER}'.format(DUMP_FOLDER=DUMP_FOLDER)

#generate dump filename
from time import strftime, localtime
timestamp     = strftime("%Y%m-%d", localtime()) #strftime format ref. http://strftime.org/
dumpFilename  = 'backup-{timestamp}.sql'.format(timestamp=timestamp)  #timestamp as YYYYmm-dd ref. http://stackoverflow.com/a/415525/248616
DUMP_FILE     = '{DUMP_HOME}/{dumpFilename}'.format(DUMP_HOME=DUMP_HOME, dumpFilename=dumpFilename)

#s3 upload path
S3_BUCKET_NAME_DEFAULT = 'robotbasecloud-dbbackup'
if not S3_BUCKET_NAME: S3_BUCKET_NAME = S3_BUCKET_NAME_DEFAULT
S3_BUCKET   = 's3://{S3_BUCKET_NAME}/{DUMP_FOLDER}'.format(S3_BUCKET_NAME=S3_BUCKET_NAME, DUMP_FOLDER=DUMP_FOLDER)
S3_DUMPFILE = '{S3_BUCKET}/{dumpFilename}'.format(S3_BUCKET=S3_BUCKET, dumpFilename=dumpFilename)
S3_LATEST   = '{S3_BUCKET}/latest.sql'.format(S3_BUCKET=S3_BUCKET, DUMP_FILE=DUMP_FILE)

#endregion input entries