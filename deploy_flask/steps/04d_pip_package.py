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

#region initials

#empty input => use default pip package file
if not PIP_REQUIREMENT:
  PIP_REQUIREMENT = PIP_REQUIREMENT_DEFAULT

#endregion initials

#region print infos & steps
infos='''
Install pip's requirements
  PIP_REQUIREMENT={PIP_REQUIREMENT}
'''.format(
  HL=HL,CM=CM,EC=EC,
  PIP_REQUIREMENT=PIP_REQUIREMENT,
)

steps='''
#Installing pip package... BEGIN

  {HL}#00. initiate sudo {EC}
  sudo echo 'sudo initiated'

  {HL}#01. install pip's ubuntu pre-requisites {EC}
    {PIP_UTIL}/install-crypto-preqs.sh
    {PIP_UTIL}/install-mysql-preqs.sh

  {HL}#02. install app's pip packages {EC}
    sudo -H pip install -r {PIP_REQUIREMENT} --ignore-installed

  {HL}#zz. aftermath check {EC}
    echo ''; echo 'Aftermath check'
    python {PYTHON_UTIL}/verify_version.py flask

#Installing pip package... END
'''.format(
  HL=HL,CM=CM,EC=EC,
  PIP_UTIL=PIP_UTIL,
  PIP_REQUIREMENT=PIP_REQUIREMENT,
  PYTHON_UTIL=PYTHON_UTIL,
)

print(infos)
print(steps)
#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun pip install'
)
