#!/usr/bin/env python2.7

#load config package
from config import *


# #region parse params
options = dict(
  shortOpts = 's:t:c:d:',
  longOpts  = ['source=', 'target=', 'caption=', 'debug='],
)

sourcePath = getArg('-s', options)
targetPath_underHome = getArg('-t', options)
caption = getArg('-c', options)
debug = getArg('-d', options)

if not (sourcePath or targetPath_underHome):
  raise Exception('{ER}Both param -s source path and -t target path are required {EC}'.format(ER=ER,EC=EC) )

if not debug: debug=False

#endregion parse params


##region build command to run

#region prepare headline
if caption:
  whatUpload = '%s at %s' % (caption, sourcePath)
else:
  whatUpload = sourcePath

headline="Uploading {whatUpload} to remote:'{targetPath}' " \
         .format(whatUpload=whatUpload, targetPath=targetPath_underHome)
#endregion prepare headline


steps= """
#do rsync
rsync -chazkP {sourcePath} {dockerRsyncURL}/{targetPath_underHome}
""".format(
  sourcePath=sourcePath,
  targetPath_underHome=targetPath_underHome,
  dockerRsyncURL=HOST_DOCKERRSYNC_URL,
)

##endregion build command to run

if debug: print(steps)

#run it
runPrintedSteps(steps, headline, COLOR=CM)
