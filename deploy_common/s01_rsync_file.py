#!/usr/bin/env python2.7

#load config package
from config import *


# #region parse params
options = dict(
  shortOpts = 's:t:c:d:',
  longOpts  = ['source=', 'target=', 'caption=', 'debug='],
)

sourcePath = getArg('-s', options)
targetPath = getArg('-t', options)
caption    = getArg('-c', options)
debug      = getArg('-d', options)

if not (sourcePath or targetPath):
  raise Exception('{ER}Both param -s source path and -t target path are required {EC}'.format(ER=ER,EC=EC) )

if not debug:
  debug=False

#endregion parse params


##region build command to run
hostKey = HOST_SSH_KEY if HOST_SSH_KEY else downloadFile(HOST_SSH_KEY_URL, chmod='600')

optCreatePath='--rsync-path="mkdir -p {targetPath} && rsync" ' \
              .format(targetPath=targetPath) #ref. http://stackoverflow.com/a/14877351/248616


#region prepare headline
if caption:
  whatUpload = '%s at %s' % (caption, sourcePath)
else:
  whatUpload = sourcePath

headline="Uploading {whatUpload} to remote:'{targetPath}' " \
         .format(whatUpload=whatUpload, targetPath=targetPath)
#endregion prepare headline


sshPort = '-p %s' % HOST_SSH_PORT if HOST_SSH_PORT else ''
steps= """
  #prepare ssh connection
  eval $(ssh-agent -s) > /dev/null
  ssh-add $hostKey > /dev/null
  
  #do rsync
  rsync -e 'ssh -i {hostKey} {sshPort}' {optCreatePath} -chazvPk {sourcePath} {HOST_USER}@{HOST_IP}:{targetPath}
""".format(
  hostKey=hostKey,
  sshPort=sshPort,
  HOST_USER=HOST_USER,
  HOST_IP=HOST_IP,

  sourcePath=sourcePath,
  targetPath=targetPath.replace(REMOTE_HOME, REMOTE_HOME_bash),

  optCreatePath=optCreatePath.replace(REMOTE_HOME, REMOTE_HOME_bash),
)

##endregion build command to run

if debug:
  print(steps)

#run it
runPrintedSteps(steps, headline, COLOR=CM)
