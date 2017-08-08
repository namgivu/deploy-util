#!/usr/bin/env python2.7
"""
Run migration script in order of timestamp in file names
- migratedb.py -m /path/to/migration/script/folder
"""

from config.common  import *
from config.input   import *
from config.initial import *

import os ; SCRIPT_HOME = os.path.abspath(os.path.dirname(__file__))


##region parse params
options = dict(
  shortOpts = 'a:f:t:m:',
  longOpts  = ['autorun=', 'from=', 'to=', 'migrationFolder='],
)

isAutorun = getArg('-a', options)

#param `from` and `to` to limit the script range to run
scriptFrom  = getArg('-f', options)
scriptTo    = getArg('-t', options)

#which folder are migration script files stored at?
migrationFolder = getArg('-m', options)
if not migrationFolder:
  migrationFolder = MIGRATION_VAULT

##endregion parse params


#region input validate
if not migrationFolder: #not provided via param => use the one in input file
  migrationFolder = MIGRATION_VAULT
  if not migrationFolder: #not defined via input file either => use default
    migrationFolder = MIGRATION_VAULT_DEFAULT
#endregion input validate


#region prepare info
info = '''
{HL}#Running migration db info{EC}
  #migrationFolder : {CM}{migrationFolder}{EC}
'''.format(
  HL=HL,CM=CM,EC=EC,
  migrationFolder=migrationFolder,
)
#endregion prepare info


#region scan for script file in `SCRIPT_VAULT` folder
SCRIPT_VAULT= migrationFolder
files = getFilesByTimestamp(
  folder=SCRIPT_VAULT,
  regexTimestamp='\d\d\d\d\d\d.\d\d-\d\d.\d\d', fileExt='.sql'
)

scriptFiles = []
for key, filePath in files.iteritems():
  #region check timestamp within given range -from and -to
  if scriptFrom and key < scriptFrom: continue
  if scriptTo   and key > scriptTo:   continue
  #endregion check timestamp within given range -from and -to

  scriptFiles.append(dict(key=key, path=filePath))
#endregion scan for script file in `SCRIPT_VAULT` folder


##region build steps to run test-case in vault
steps = ''

optConnection = '--defaults-extra-file=%s' % DB_CONN
mysqlCmd='mysql {optConnection} {DB_NAME}'.format(
  optConnection=optConnection,
  DB_NAME=DB_NAME,
)

#region prepare run script file
runScriptCmd = ''
for i,d in enumerate(scriptFiles): #foreach with index ref. http://stackoverflow.com/a/28072982/248616
  sh = '''  printf 'Run {i}/{n} {scriptKey}... ' 
  {mysqlCmd} < {scriptFile} ; echo '{eCM}done{eEC}'
'''.format(
    eCM=eCM,eEC=eEC,
    i=i+1, n=len(scriptFiles),
    mysqlCmd=mysqlCmd,
    scriptKey=d['key'],
    scriptFile=d['path'],
  )

  #make it tiny via using variable
  sh = sh.replace(SCRIPT_HOME,    '$h')
  sh = sh.replace(SCRIPT_VAULT,   '$v')
  sh = sh.replace(optConnection,  '$c')

  runScriptCmd += sh
#endregion prepare run script file

#no script found message
if not runScriptCmd:
  runScriptCmd = '  (no script found at %s) - you may want to set another path via -m param' % MIGRATION_VAULT

steps += '''
{HL}#Command to run scripts{EC}
  {CM}#prepare variable{EC}
  export h='{SCRIPT_HOME}' ; #SCRIPT_HOME
  export v='{SCRIPT_VAULT}' ; #SCRIPT_VAULT
  export c='{conn}'; #connection

  {CM}#run migration files{EC}
  {runScriptCmd}
'''.format(
  HL=HL,CM=CM,EC=EC,
  SCRIPT_HOME=SCRIPT_HOME,
  SCRIPT_VAULT=SCRIPT_VAULT,
  conn=optConnection,
  runScriptCmd=runScriptCmd.strip(),
)

##endregion build steps to run test-case in vault

#printing
print(info)
print(steps)

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun migratedb'
)
