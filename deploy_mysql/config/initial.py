#!/usr/bin/env python2.7
from common import *
from input  import *


##region input validate

#no param for `db name` exists => set ad deploy id or default name
if not DB_NAME:
  from deploy_flask.steps.input_0th import DEPLOY_ID
  DB_NAME = DEPLOY_ID if    DEPLOY_ID \
                      else  DB_NAME_DEFAULT

#region check if `db host` is a `localhost@remote-ip`
remoteLocalhost= 'localhost@'
if remoteLocalhost in DB_HOST:
  #extract ip
  remoteIP = DB_HOST.replace(remoteLocalhost, '')

  #notice user
  print('''
{HL}NOTICE{EC}
The DB_HOST is set under formation as {HL}localhost@remote-ip{EC}
which means it's required to
- ssh connect to remote site at ip={ER}{remoteIP}{EC}
- this utility is uploaded & run there
  '''.format(
    HL=HL,ER=ER,EC=EC,
    remoteIP=remoteIP,
  ).rstrip() )

  #get confirmed being on remote site to continue
  print('''
We are on remote site ip={ER}{remoteIP}{EC} ? (y/N)
  '''.format(
    HL=HL,ER=ER,EC=EC,
    remoteIP=remoteIP,
  ).rstrip() )
  yes = raw_input().lower() == 'y'
  if not yes:
    #region print guideline to go next
    print('''
{ER}Please rsync utility folder to remote site and try again over there{EC}
You may run below commands to do so
  #rsync utility folder
  {UTILITY_ROOT}/deploy_flask/steps/01z_applied.py -a 1
  #ssh to remote site
  {UTILITY_ROOT}/deploy_flask/steps/00_ssh_connect.py -a 1

  #TODO Print ssh command that `remote execute` the current-running command; so that we don't need those 2 steps above

'''.format(
      ER=ER,EC=EC,
      UTILITY_ROOT=UTILITY_ROOT,
    ))
    #endregion print guideline to go next

    sys.exit()

  #set it localhost as normal
  DB_HOST='localhost'
#endregion check if `db host` is a `localhost@remote-ip`

##endregion input validate


#region prepare db connection at file DB_CONN
sh='''
#create mysqlConn file from template
cp -f {DB_CONN_TEMPLATE} {DB_CONN}

#fill in the template with db info
export template='{DB_CONN}'
key='host'      && sed -i -e "s|$key[ ]*=.*$|$key = {DB_HOST}|g" $template
key='user'      && sed -i -e "s|$key[ ]*=.*$|$key = {DB_USER}|g" $template
key='password'  && sed -i -e "s|$key[ ]*=.*$|$key = {DB_PASS}|g" $template
'''.format(
  DB_CONN_TEMPLATE=DB_CONN_TEMPLATE,
  DB_CONN=DB_CONN,
  DB_HOST=DB_HOST,
  DB_USER=DB_USER,
  DB_PASS=DB_PASS,
)

run_bash(sh)
#endregion prepare db connection at file DB_CONN


#default db migration script location
from deploy_flask.steps.input import CODE_HOME
MIGRATION_VAULT_DEFAULT= '%s/util/sql/data-migration' % CODE_HOME
if not MIGRATION_VAULT:
  MIGRATION_VAULT = MIGRATION_VAULT_DEFAULT
