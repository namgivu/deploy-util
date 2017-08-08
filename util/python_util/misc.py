from common import *


def getArg(name, options):
  #TODO Upgrade to use this parser ref. https://docs.python.org/3/library/argparse.html#module-argparse

  """
  Parse command line arguments ref. https://www.tutorialspoint.com/python/python_command_line_arguments.htm
  E.g.
    - From cmd line
    $ YOUR_CODE.py -a 1 -c ls -v --autorun=122

    - In YOUR_CODE.py
    ...
    getArg(-a, shortOpts, longOpts)
    ...

    - Parsed outcome
    avPairs = [('-a', '1'), ('-c', 'ls'), ('-v', ''), ('--autorun', '122')]

  """

  shortOpts = options['shortOpts']
  longOpts  = options['longOpts']

  #get params data
  import sys
  argv = sys.argv[1:]

  #region parse params data
  import getopt
  try:
    avPairs, leftAfter = getopt.getopt(argv, shortOpts, longOpts)
  except Exception as e:
    raise e
  #endregion parse params data

  found=None
  #region find value
  for arg,value in avPairs:
    if arg==name:
      found=value
      break
  #endregion find value

  return found


##region run_bash
#TODO `source something` not work, why?
'''
Run external bash .sh script from Python code
'''
import subprocess


def run_bash(bashCmd):
  return subprocess.call(bashCmd, shell=True) #get error code ref. http://stackoverflow.com/a/8724601/248616


def orun_bash(bashCmd):
  output = subprocess.check_output(bashCmd.split(' ') )
  return output
##endregion run_bash


def download_from_s3(bucket, filename, saveTo, s3Key, s3Secret):
  #connect bucket
  import boto
  conn = boto.connect_s3(s3Key, s3Secret)
  b = conn.get_bucket(bucket)

  #get bucket key form filename
  key = b.get_key(filename)

  #download
  key.get_contents_to_filename(saveTo)


def grep(pattern, filePath):
  """
  bash's grep version in python
  ref. http://stackoverflow.com/a/26659479/248616
  """

  with open(filePath, 'r') as f:
    #read file content
    string = f.read()

    #do grep
    import re
    found = re.findall(pattern, string)

    return found[0]


##region mysql util
def makeMySqlCmd(mysqlConnFile, verbose):
  """password loaded from config file"""
  mysqlCmd = 'mysql --defaults-extra-file={mysqlConnFile} {verbose}'.format(
    mysqlConnFile=mysqlConnFile,
    verbose='-v' if verbose else ''
  )
  return mysqlCmd


def str2file(sql):
  """
  Write sql string to file ref. http://stackoverflow.com/a/5214587/248616
  """
  from tempfile import mktemp
  localPath = mktemp()

  f = open(localPath, 'w')
  f.write(sql)
  f.close()

  return localPath


#region bash 2 run sql utils
def escapeBackStick(sql):
  return sql.replace('`','\`')


def regexReplace(s, old, new):
  """replace string using regex ref. http://stackoverflow.com/a/5658439/248616"""
  import re
  t = re.sub(old, new, s, flags=re.M) #re.M to use ^ for begin-of-line
  return t


def bash2RunSql(sql, mysqlConnFile, dbName, verbose=False):
  #make mysql cmd
  mysqlCmd = makeMySqlCmd(mysqlConnFile, verbose)

  #run it via bash's mysql
  sh = '{mysqlCmd} {dbName} -e "{sql}" '.format(
    mysqlCmd=mysqlCmd,
    dbName=dbName if dbName else '',
    sql=sql,
  )
  sh = escapeBackStick(sh)
  return sh


def bash2RunSqlMulp_viaTempFile(sql, mysqlConnFile, dbName, verbose=False):
  sqlFile = str2file(sql)
  sh = bash2RunSqlFile(sqlFile, mysqlConnFile, dbName, verbose)
  sh = escapeBackStick(sh)
  return sh


def bash2RunSqlMulp(sql, mysqlConnFile, dbName, verbose=False):
  sql = regexReplace(sql, r'^[ ]*#.*', '') #remove comment lines
  sql = sql.replace('\n', ' ') #replace newline by space to run in bash

  sh = []
  for cmd in sql.split(';'):
    cmd = cmd.strip()
    if not cmd: continue
    sh.append(bash2RunSql(cmd, mysqlConnFile, dbName, verbose) )
  sh = '\n'.join(sh)
  return sh


def bash2RunSqlFile(file2Run, mysqlConnFile, dbName, verbose=False):
  #make mysql cmd
  mysqlCmd = makeMySqlCmd(mysqlConnFile, verbose)

  #run it via bash's mysql
  sh = '{mysqlCmd} {dbName} < {script2Run}'.format(
    mysqlCmd=mysqlCmd,
    dbName=dbName if dbName else '',
    script2Run=file2Run,
  )
  sh = escapeBackStick(sh)
  return sh
#endregion bash 2 run sql utils


#region do run sql
def sqlRunFile(scriptFile, mysqlConnFile, dbName, verbose=False):
  sh = bash2RunSqlFile(scriptFile, mysqlConnFile, dbName, verbose)
  run_bash(sh)


def sqlRun(sql, mysqlConnFile, dbName, verbose=False):
  """Run sql script that is a SINGLE-commands batch"""
  scriptFile = str2file(sql)
  sqlRunFile(scriptFile, mysqlConnFile, dbName, verbose)


def sqlRunMulp(sql, mysqlConnFile, dbName, verbose=False):
  """Run sql script that is a MULTIPLE-commands batch"""
  scriptFile = str2file(sql)
  sqlRunFile(scriptFile, mysqlConnFile, dbName, verbose)


def sqlShowTables(mysqlConnFile, dbName):
  sqlRunMulp('show tables;', mysqlConnFile, dbName)
#endregion do run sql


##endregion mysql util


#region file utils
def getFileSize(path):
  """Get file size at a given path"""

  #translate ~ ie. user home folder ref. http://stackoverflow.com/a/4028943
  from os.path import expanduser
  path = expanduser(path)

  #get size ref. http://stackoverflow.com/a/6591957/248616
  import os
  sz = os.path.getsize(path)
  sz = readableNum(sz)
  return sz


def readableNum(num, suffix='b'):
  """
  ref. http://stackoverflow.com/a/1094933/248616
  """
  for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
    if abs(num) < 1024.0:
      return "%3.1f%s%s" % (num, unit, suffix)
    num /= 1024.0

  return "%.1f%s%s" % (num, 'Y', suffix)


def renameFile(fullPath, newFilename):
  #keep the folder
  import os
  folder = os.path.dirname(fullPath)

  #do rename
  newFullPath = os.path.join(folder, newFilename)
  os.rename(fullPath, newFullPath)

  return newFullPath
#endregion file utils


def runPrintedSteps(steps, headline='Running command', COLOR=DK):
  #remove color code in steps
  sh=steps\
    .replace(HL,'') \
    .replace(CM,'') \
    .replace(EC,'') \
    .replace(ER,'')

  #run it
  print '\n{COLOR}#{headline}... BEGIN {EC}\n'.format(COLOR=COLOR,EC=EC, headline=headline)
  run_bash(sh)
  print '\n{COLOR}#{headline}... END   {EC}\n'.format(COLOR=COLOR,EC=EC, headline=headline)


def downloadFile(url, downloadTo=None, chmod=None):
  #validate downloaded filename ie. downloadTo
  if not downloadTo: #filename empty => generate random path
    from tempfile import mktemp
    downloadTo = mktemp()

  #do download ref. http://stackoverflow.com/a/22776/248616
  import urllib ; urllib.urlretrieve(url, filename=downloadTo)

  #set permission in `chmod` param
  if chmod:
    run_bash('chmod %s %s' % (chmod, downloadTo))

  return downloadTo


def getFilesByTimestamp(folder, regexTimestamp='\d\d\d\d\d\d.\d\d-\d\d\.\d\d', fileExt=None):
  """
  Get all file under containing folder `folder` which has timestamp in their filename
  matched with regex/regular expression `regexTimestamp` and has filename extension as `fileExt`
  """

  #region get all file in vault
  allFiles = []
  import os
  for root, dirs, files in os.walk(folder):
    for f in sorted(files):
      allFiles.append(os.path.join(root, f))
  #endregion get all file in vault

  ##region check extension in filename
  if fileExt:  #not empty meaning we need to check
    #remove dot '.' in filter
    fileExt = fileExt.replace('.', '')

    #region do filter
    a = []
    for f in allFiles:
      try:
        ext = f.split('.')[-1]
        if ext == fileExt:
          a.append(f)
      except Exception as e:
        raise Exception('Cannot get file extension of path %s\nError:%s' % (f, str(e)))
    #endregion do filter

    #save back the file list after filtered
    allFiles = a
  ##endregion check extension in filename

  #region make dict d={key : filePath} where key=$timestamp-$filename
  d = dict()
  for f in allFiles:
    try:
      filename = f.split('/')[-1]
    except Exception as e:
      raise Exception('Cannot get filename of path %s\nError:%s' % (f, str(e)))

    import re;
    regex = re.compile(regexTimestamp)  #pattern of timestamp ref. https://gist.github.com/dideler/5219706
    for timestamp in re.findall(regex, f):
      key = '%s-%s' % (timestamp, filename)
      d[key] = f
      break
  #endregion make dict d={key : filePath} where key=$timestamp-$filename

  #sort d by key ref. http://stackoverflow.com/a/9001529/248616
  import collections
  od = collections.OrderedDict(sorted(d.items()))

  return od


#region github ssh key file
def makeGithubKeyFilename(DEPLOY_ID):
  filename = 'github.%s' % DEPLOY_ID
  return filename


def getRemoteGithubKey(REMOTE_GITHUB_PATH, DEPLOY_ID):
  filename = makeGithubKeyFilename(DEPLOY_ID)
  keyPath = '%s/%s' % (REMOTE_GITHUB_PATH, filename)
  return keyPath
#endregion github ssh key file


def isSSL(port):
  return str(port) == '443'
