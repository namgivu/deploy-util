#!/usr/bin/env python2.7

"""
Usage
  #create db from S3 script file - the latest one
  python inidb.py

  #full options
  python inidb.py $options
  where $options = [
    -s /path/to/backup/script/file  #option to pickup backup script file
    -d database_name                #option to set database name
    -c /path/to/connection/file     #option to pickup connection file e.g. `mysql-connection.LOCAL`
  ]
"""

from config.common  import *
from config.input   import *
from config.initial import *


#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options)
#endregion parse params


steps = ''

#region handle scriptFile
SCRIPT_FILE_DOWNLOAD = None
if not SCRIPT_FILE: #no param for `backup script` exists => get form S3
  #region confirm before download from s3
  s = '''
Backup script NOT provided
Download it from S3 (y/N)?'''.format(
    eCM=eCM, eEC=eEC
  ) ; print(s)

  yes=raw_input().lower() == 'y'
  if not yes:
    sys.exit()
  #endregion confirm before download from s3

  #region download script from s3
  SCRIPT_FILE_DOWNLOAD ='/tmp/%s.sql' % DB_NAME
  steps += '''
  #{HL}Download script from s3{EC}
    aws s3 cp s3://{DB_LATEST_BACKUP} {SCRIPT_FILE_DOWNLOAD}
    #S3 script file saved to {CM}{SCRIPT_FILE_DOWNLOAD}{EC}
    ls -la {SCRIPT_FILE_DOWNLOAD}
  '''.format(
    HL=HL,CM=CM,EC=EC,
    DB_LATEST_BACKUP=DB_LATEST_BACKUP,
    SCRIPT_FILE_DOWNLOAD=SCRIPT_FILE_DOWNLOAD,
  )
  #endregion download script from s3

scriptFile = SCRIPT_FILE if SCRIPT_FILE \
                       else SCRIPT_FILE_DOWNLOAD

#endregion handle scriptFile


##region info printing asset
info = ''

#region get info prepared
if SCRIPT_FILE:
  downloadedNote = ''
else:
  downloadedNote = '{CM}#downloaded from S3 at "{DB_LATEST_BACKUP}" {EC}'.format(
    CM=CM,EC=EC,
    DB_LATEST_BACKUP=DB_LATEST_BACKUP,
  )

grepDB_CONN='''
    #grep check {CM}
    {grepH}
    {grepU}
    {grepP} {EC}
'''.format(
  CM=CM,EC=EC,
  grepH = grep(    'host[ ]*=.*', DB_CONN).strip(),
  grepU = grep(    'user[ ]*=.*', DB_CONN).strip(),
  grepP = grep('password[ ]*=.*', DB_CONN).strip(),
)

printedSCRIPT_FILE = '%s %s%s' % (
  getFileSize(scriptFile), scriptFile, downloadedNote
)
#endregion get info prepared

info = '''
{HL}#Init db info{EC}
  DB_NAME = {ER}{DB_NAME}{EC}
  DB_HOST = {CM}{DB_HOST}{EC}
  DB_USER = {CM}{DB_USER}{EC}
  DB_PASS = {CM}{DB_PASS}{EC}
  aka. {CM}{DB_USER}:{DB_PASS}{EC}@{CM}{DB_HOST}{EC}/{ER}{DB_NAME}{EC}

  DB_CONN = {DB_CONN}
{grepDB_CONN}

  SCRIPT_FILE = {ER}{printedSCRIPT_FILE}{EC}
'''.format(
  HL=HL,CM=CM,ER=ER,EC=EC,
  DB_NAME=DB_NAME,
  DB_HOST=DB_HOST,
  DB_USER=DB_USER,
  DB_PASS=DB_PASS,
  DB_CONN=DB_CONN,

  grepDB_CONN=grepDB_CONN.rstrip(),
  printedSCRIPT_FILE=printedSCRIPT_FILE,
)

##endregion info printing asset


#region create db entry
sql = '''
  drop database IF EXISTS `{DB_NAME}`;
  create database `{DB_NAME}` DEFAULT CHARACTER SET utf8;
'''.format(DB_NAME=DB_NAME)

sh=''

for s in sql.split(';'):
  s = s.strip()
  if s:
    sh += '  %s\n' % bash2RunSql(s, DB_CONN, dbName=None)

steps += '''
{HL}#Create db entry{EC}
echo 'Create db entry...'
{sh}
'''.format(
  HL=HL,CM=CM,EC=EC,
  sh=sh,
)
#endregion create db entry

#region restore db
steps += '''
{HL}#Restore db{EC}
echo 'Restore db...'
{sh}
'''.format(
  HL=HL,CM=CM,EC=EC,
  sh=bash2RunSqlFile(scriptFile, mysqlConnFile=DB_CONN,dbName=DB_NAME),
)
#endregion restore db

#region aftermath check
steps += '''
{HL}#Aftermath check{EC}
echo 'Aftermath check...'
{sh}
'''.format(
  HL=HL,CM=CM,EC=EC,
  sh=bash2RunSql('show tables;', DB_CONN, DB_NAME)
)
#endregion aftermath check


print(info)
print(steps)

if isAutorun: runPrintedSteps(
  steps, headline='Autorun initdb'
)

print(info) #yeah, we print it again; useful for reading at the end when autorun
