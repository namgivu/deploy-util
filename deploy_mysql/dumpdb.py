#!/usr/bin/env python2.7
"""
Usage
- print steps
  dumbdb.py

- print & autorun dumping
  dumbdb.py -a 1

- print dumping; also include step to download dumped file to local path
  dumbdb.py  -d /path/to/save/dumped/file.sql
"""

from config.input_dumpdb  import *
from config.initial       import *

#region parse params
options = dict(
  shortOpts = 'a:d:',
  longOpts  = ['autorun=', 'download2LocalAt='],
)

isAutorun = getArg('-a', options)
download2LocalPath = getArg('-d', options) #where to store the dumped file on local machine
#endregion parse params

#mysql & aws s3 version
from util.python_util.misc import orun_bash
MYSQL_VERSION = orun_bash('mysql -V').strip()
AWSS3_VERSION = orun_bash('which aws').strip()
#AWSS3_VERSION = orun_bash('aws s3 --version').strip() #This is output of 'which aws' #TODO Why can't we catch output of this command?

##region print infos & steps

#region prepare info
infos='''
{HL}#Info of dumping database{EC}
  DB_NAME={CM}{DB_NAME}{EC}

  DB_CONN={CM}{DB_CONN}{EC}
  Details
  {CM}{catDB_CONN}{EC}

  {CM}#Verify MySQL version (must be 5.7 or later){EC}
  {MYSQL_VERSION}
  {CM}#Verify 'aws s3' installed {EC}
  {AWSS3_VERSION} #TODO Why we can't get python print out 'aws s3 --version'
'''.format(
  HL=HL,CM=CM,EC=EC,
  DB_NAME=DB_NAME,
  DB_CONN=DB_CONN,
  catDB_CONN=orun_bash('cat %s' % DB_CONN),
  MYSQL_VERSION=MYSQL_VERSION,
  AWSS3_VERSION=AWSS3_VERSION,
)
#endregion prepare info


#region setup options
'''
Note:
We set it up with NO_DB_NAME so as to have NO 'create database' command in dumped outcome
ref. http://stackoverflow.com/a/9074489/248616
'''
optConnection = '--defaults-extra-file=%s' % DB_CONN
optRoutine    = '--routines' #also dump routines/stored-proc ref. http://stackoverflow.com/a/5075216/248616

options = '{optConnection} {optRoutine} {verbose}'.format(
  optConnection=optConnection,
  optRoutine=optRoutine,
  verbose='-v' if MYSQL_DEBUG else ''
)
#endregion setup options


steps=''


#region dump main
steps += '''
{HL}#Dump database to file{EC}
  {CM}#prepare dumped location{EC}
  mkdir -p {DUMP_HOME}/ ; rm -rf {DUMP_FILE}

  {CM}#Do dumping database to file{EC}
  echo '{eCM}Dumping database "{DB_NAME}" BEGIN{eEC}\n'
  mysqldump {options} {DB_NAME} > {DUMP_FILE}

  #check if dumping succeed
  if [ $? -ne 0 ]; then
  echo '{eER}Error occurred{eEC}'
    exit
  fi

  echo 'Database dumped at file {eER}{DUMP_FILE}{eEC}'
  ls -la {DUMP_FILE}
  echo
  echo '{eCM}Dumping database "{DB_NAME}" END{eEC}\n'

  {CM}#Some extra post-dumping tune{EC}
    {CM}#remove definer of sp/routine/stored procedure create command{EC}
    sed -i -e 's|CREATE DEFINER=[^ ]* PROCEDURE|CREATE PROCEDURE|g' {DUMP_FILE}

    {CM}#remove definer of CREATE VIEW command{EC}
    sed -i -e 's|50013 DEFINER=[^ ]* SQL SECURITY DEFINER||g' {DUMP_FILE}

    {CM}#aftermath check{EC}
    cat {DUMP_FILE} | grep -iE 'CREATE DEFINER|50013 DEFINER'
'''.format(
  HL=HL,CM=CM,EC=EC,
  eHL=eHL,eCM=eCM,eEC=eEC,eER=eER,

  DUMP_HOME=DUMP_HOME,
  DUMP_FILE=DUMP_FILE,

  DB_NAME=DB_NAME,
  options=options,
  NO_DB_NAME='',
)
#endregion dump main


#region s3 transfer
steps += '''
{HL}#Transfer vs S3{EC}
  echo
  echo '{eCM}Transfer vs S3 BEGIN{eEC}'
  echo

  {CM}#Upload dumped file to S3{EC}
  aws s3 cp {DUMP_FILE} {S3_DUMPFILE}
  echo

  {CM}#Also update the latest entry{EC}
  aws s3 cp {S3_DUMPFILE} {S3_LATEST}
  echo

  {CM}#Aftermath check{EC}
  echo
  echo '{eCM}Aftermath check{eEC}'

    echo 'The outcome'
    echo '{eER}{S3_DUMPFILE}{eEC}'
    echo '{eER}{S3_LATEST}{eEC}'
    echo

    echo 'Listed on S3'
    aws s3 ls {S3_DUMPFILE}
    aws s3 ls {S3_LATEST}

  echo
  echo '{eCM}Transfer vs S3 END{eEC}'
'''.format(
  HL=HL,CM=CM,EC=EC,
  eHL=eHL,eCM=eCM,eEC=eEC,eER=eER,

  DUMP_FILE=DUMP_FILE,
  S3_DUMPFILE=S3_DUMPFILE,
  S3_LATEST=S3_LATEST,
)

#endregion s3 transfer

#region handle download2LocalPath step
if download2LocalPath:
  steps += '''
  {CM}#(from-local, optional) Download dumped file to local{EC}
  aws s3 cp {S3_DUMPFILE} {download2LocalPath}
  '''.format(
    HL=HL, CM=CM, EC=EC,
    S3_DUMPFILE=S3_DUMPFILE,
    download2LocalPath=download2LocalPath,
  )
#endregion handle download2LocalPath step


print(infos)
print(steps)
##endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun dumpdb'
)
