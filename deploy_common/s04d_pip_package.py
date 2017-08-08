#!/usr/bin/env python2.7

#load config package
from config import *

#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options)
#endregion parse params


PIP_REQUIREMENT = '%s/requirements.txt' % CODE_HOME


#region print infos & steps
infos='''
Install pip's requirements
PIP_REQUIREMENT={CM}{PIP_REQUIREMENT}{EC}
'''.format(
  HL=HL,CM=CM,EC=EC,
  PIP_REQUIREMENT=PIP_REQUIREMENT,
)

steps='''
#Installing pip package... BEGIN

  {CM}#initiate sudo {EC}
  sudo echo 'sudo initiated'

  {CM}#install pip's ubuntu pre-requisites {EC}
  sudo -H apt-get install -y build-essential libssl-dev libffi-dev python-dev
  sudo -H apt-get install -y libmysqlclient-dev

  {CM}#install app's pip packages {EC}
  sudo -H pip install -r {PIP_REQUIREMENT} --ignore-installed

#Installing pip package... END
'''.format(
  HL=HL,CM=CM,EC=EC,
  PIP_REQUIREMENT=PIP_REQUIREMENT,
)

print(infos)

if not isAutorun:
  print(steps)

#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun pip install'
)
