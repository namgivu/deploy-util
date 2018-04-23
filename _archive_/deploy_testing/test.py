#!/usr/bin/env python2.7

from config import *

#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options) #TODO Why passing --autorun=1 NOT working, while --verbose=1 works?
#endregion parse params


#region print infos & steps

infos='''
Install steps for selenium infrastructure
'''


steps='''
{CM}#command to set up selenium infrastructure{EC}
dth={DEPLOY_TESTING_HOME}
$dth/s03a1_install-Xvfb.py -a 1
$dth/s03a2_install-selenium-infras.py -a 1
$dth/s03b_install-chromedriver.py -a 1
$dth/s03c_install-chrome-headless.py -a 1
$dth/s03z_test-selenium-webdriver-chrome.py -a 1
'''.format(
  ER=ER,HL=HL,CM=CM,EC=EC,
  DEPLOY_TESTING_HOME=DEPLOY_TESTING_HOME,
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps

if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
