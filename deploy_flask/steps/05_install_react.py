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


#npm's webpack config
NPM_CONFIG = '%s/webpack.config.js' % APP_FRONTEND


#region print infos & steps
infos='''
{HL}We install REACT{EC}
  APP_FRONTEND       : {CM}{APP_FRONTEND}{EC}
  REACT_LOCAL_CONFIG : {CM}{REACT_LOCAL_CONFIG}{EC}
'''.format(
  HL=HL,CM=CM,EC=EC,
  APP_FRONTEND=APP_FRONTEND,
  REACT_LOCAL_CONFIG=REACT_LOCAL_CONFIG,
)

steps='''
#Installing REACT... BEGIN

  {HL}#initiate sudo {EC}
  {SUDO} echo 'sudo initiated'

  {HL}#Install npm {EC}
    {CM}#install REACT {EC}
    {SUDO} apt install -y npm

    {CM}#register binary ref. https://github.com/nodejs/node-v0.x-archive/issues/3911#issuecomment-8956154 {EC}  export bin_nodejs='/usr/bin/nodejs'
    {SUDO} ln -f -s /usr/bin/nodejs /usr/bin/node

  {HL}#Install REACT {EC}
  export curDir=`pwd`
  cd {APP_FRONTEND}

    {CM}#REACT install {EC}
    npm install

    {CM}#REACT npm config {EC}
    cp -f {NPM_CONFIG_TEMPLATE} {NPM_CONFIG}
    
    {CM}#REACT generate app.js {EC}
    ./node_modules/.bin/webpack {NPM_DEBUG_BUILD}
    
  cd $curDir

  {HL}#Aftermath check {EC}
  echo ; echo 'Testing REACT local config'
  cat {NPM_CONFIG} | grep serverUrl

#Installing REACT... END
'''.format(
  HL=HL,CM=CM,EC=EC,

  SUDO='sudo -H',
  APP_FRONTEND=APP_FRONTEND,
  NPM_CONFIG_TEMPLATE=NPM_CONFIG_TEMPLATE,
  NPM_CONFIG=NPM_CONFIG,
  NPM_DEBUG_BUILD='-d' if NPM_DEBUG_BUILD else '',
)


print(infos)
print(steps)
#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun installing REACT'
)
