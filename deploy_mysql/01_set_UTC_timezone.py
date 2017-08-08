#!/usr/bin/env python2.7

from config.common import * #initiate common asset
from config.input  import * #load the inputs
from config.initial import *

#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options)
#endregion parse params

#region print infos & steps
sql = """
#set mysql timezone
set @@global.time_zone='+00:00';

#aftermath check
SELECT TIMEDIFF(NOW(), UTC_TIMESTAMP);
select 
  now()               as 'current-time of mysql timezone',
  UTC_TIMESTAMP 		  as 'current-time of UTC ie. timezone 00',
  @@global.time_zone	as 'mysql timezone',
  ''
;
"""
sh=bash2RunSqlMulp(sql, mysqlConnFile=DB_CONN, dbName=DB_NAME)

steps='''
{HL}#Set mysql timezone to be UTC ie. +00:00 timezone{EC} ref. http://stackoverflow.com/a/19075291/248616
{sh}
'''.format(
  HL=HL,CM=CM,EC=EC,ER=ER,
  sh=sh,
)
print(steps)
#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun YOUR_STEPS'
)
