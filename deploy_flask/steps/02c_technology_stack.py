#!/usr/bin/env python2.7

from common   import * #initiate common asset
from input    import * #load the inputs

#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options)
#endregion parse params

#region print steps
steps='''
#Installing technology stack... BEGIN

  {HL}#00.initiate sudo {EC}
  {sudo} echo 'sudo initiated'

  {HL}#1.update os {EC}
  {sudo} {BASH_UTIL}/update-os.sh

  {HL}#2.python {EC}
  {BASH_UTIL}/install-python.sh

  {HL}#2b.python pip {EC}
  {sudo} {BASH_UTIL}/install-pip.sh

  {HL}#3.venv {EC}
  {BASH_UTIL}/install-virtualenv.sh

  {HL}#4.LAMP {EC}
  {BASH_UTIL}/install-LAMP.sh {ER}#TODO separate this step on a single file since when done, it will not continue below steps{EC}

  {HL}#5.apache wsgi {EC}
  {BASH_UTIL}/install-Apache-WSGI.sh

  {HL}#6.aws s3 {EC}
  {BASH_UTIL}/install-AWS-CLI.sh

  {HL}#7.aftermath check {EC}
  echo ; python '{PYTHON_UTIL}/verify_version.py' os

  echo ; python '{PYTHON_UTIL}/verify_version.py' python
  echo ; python '{PYTHON_UTIL}/verify_version.py' pip
  echo ; python '{PYTHON_UTIL}/verify_version.py' virtualenv

  echo ; python '{PYTHON_UTIL}/verify_version.py' mysql
  echo ; python '{PYTHON_UTIL}/verify_version.py' apache2
  echo ; python '{PYTHON_UTIL}/verify_version.py' apache-wsgi

#Installing technology stack... END
'''.format(
  HL=HL,CM=CM,EC=EC,ER=ER,
  sudo='sudo -H',
  BASH_UTIL=BASH_UTIL,
  PYTHON_UTIL=PYTHON_UTIL,
)

print(steps)
#endregion print steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun installing technology stack'
)
