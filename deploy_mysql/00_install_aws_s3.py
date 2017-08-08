#!/usr/bin/env python2.7

from config.common import * #initiate common asset
from config.input  import * #load the inputs
from config.initial import *
from config.s3_key import * #load the inputs

#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options)
#endregion parse params

#region print infos & steps
steps='''
#Install and config aws cli BEGIN

  {HL}#install aws cli{EC}
  sudo apt-get install -y awscli

  {HL}#config aws cli{EC}
  aws configure
  {CM}#Provide below credentials when asked{EC}
    #AWS Access Key ID      {ER}{AWS_ACCESS_KEY_ID}{EC}
    #AWS Secret Access Key  {ER}{AWS_SECRET_ACCESS_KEY}{EC}
    #Default region name    {ER}{DEFAULT_REGION_NAME}{EC}
    #Default output format  {ER}{DEFAULT_OUTPUT_FORMAT}{EC}

#Install and config aws cli END
'''.format(
  HL=HL,CM=CM,EC=EC,ER=ER,
  AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID,
  AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY,
  DEFAULT_REGION_NAME=DEFAULT_REGION_NAME,
  DEFAULT_OUTPUT_FORMAT=DEFAULT_OUTPUT_FORMAT,
)

print(steps)
#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun YOUR_STEPS'
)
