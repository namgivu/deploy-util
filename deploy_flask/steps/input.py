#!/usr/bin/env python2.7
pass

#common entries
from common import *
pass

#entries from `input 0th`
from input_0th import *
pass


##region entries for `referring input`
"""Sub input = The input entries that were inferred from `input 0th` """
if not DEPLOY_ID:
  DEPLOY_ID = '%s.%s' % (APP_NAME, DEPLOY_TARGET)

WWWROOT_HOME      = '/var/www'
DEPLOY_WWWROOT    = '%s/%s' % (WWWROOT_HOME, DEPLOY_ID)

APP_CODE          = '%s' % CODE_HOME
APP_FRONTEND      = '%s/frontend' % APP_CODE
APP_PUBLIC_PATHS  = [
  '%s/app/static' % DEPLOY_WWWROOT,
]

WSGIScriptAlias   = '{DEPLOY_WWWROOT}/application.wsgi'.format(DEPLOY_WWWROOT=DEPLOY_WWWROOT)

SITE_ID               = '{DEPLOY_ID}.master'.format(DEPLOY_ID=DEPLOY_ID)
SITES_AVAILABLE       = '/etc/apache2/sites-available'
SITE_CONFIG_TEMPLATE  = '{DEPLOY_CONFIG}/apache-site'.format(DEPLOY_CONFIG=DEPLOY_CONFIG)
SITE_CONFIG_GEN       = '{DEPLOY_CONFIG}/gen/apache-site'.format(DEPLOY_CONFIG=DEPLOY_CONFIG)
SITECONF_MASTER       = 'master.conf'
SITECONF_SUB00        = 'sub00_base.conf'
ServerAdmin           = 'admin@autonomousbrain.com'

#local config for Flask app
RBS_LOCAL_CONFIG          = '{APP_CODE}/config_local.py'.format(APP_CODE=APP_CODE)
RBS_LOCAL_CONFIG_TEMPLATE = '{DEPLOY_CONFIG}/rbs-local-config/config_local.py'.format(DEPLOY_CONFIG=DEPLOY_CONFIG)

#local config for REACT frontend
NPM_CONFIG_TEMPLATE = '{DEPLOY_CONFIG}/frontend-react/webpack.config.js'\
                      .format(DEPLOY_CONFIG=DEPLOY_CONFIG,
                              DEPLOY_TARGET=DEPLOY_TARGET
                              )
REACT_LOCAL_CONFIG  = NPM_CONFIG_TEMPLATE

#when github key is provided via url, we name it as follow
DOWNLOAD_GITHUB_KEY = makeGithubKeyFilename(DEPLOY_ID)

REMOTE_CERT_FILE = "%s/%s.crt" % (REMOTE_SSL_HOME, DEPLOY_ID)
REMOTE_CERT_KEY  = "%s/%s.key" % (REMOTE_SSL_HOME, DEPLOY_ID)
DEPLOY_HTTP = 'https' if isSSL(DEPLOY_PORT) else 'http'

NPM_DEBUG_BUILD = False #True/False for building app.js webpack with/without debug info

#region extract github ssh related section
splits00 = CODE_GIT_REPO.split(':')
if len(splits00)>0:
  splits22 = splits00[0].split('@')
  if len(splits22) > 0:
    CODE_GIT_REPO_USER = splits22[0]
    CODE_GIT_REPO_HOST = splits22[1]
#endregion extract github ssh related section

#remote 's github ssh key
REMOTE_GITHUB_KEY  = getRemoteGithubKey(REMOTE_SSH_HOME, DEPLOY_ID)

##endregion entries for `referring input`


#region validate input
if not CODE_GITHUB_KEY and not CODE_GITHUB_KEY_URL:
  raise Exception('Either CODE_GITHUB_KEY or CODE_GITHUB_KEY_URL is required')

if not HOST_SSH_KEY and not HOST_SSH_KEY_URL:
  raise Exception('Either HOST_SSH_KEY or HOST_SSH_KEY_URL is required')

pass
#endregion validate input


#region info printing
printedSSLCert = '''
                  {REMOTE_CERT_FILE}
                  {REMOTE_CERT_KEY}
'''.format(
  REMOTE_CERT_FILE=REMOTE_CERT_FILE,
  REMOTE_CERT_KEY=REMOTE_CERT_KEY,
)
if DEPLOY_PORT != '443': printedSSLCert=''

FLASK_DEPLOY_INFO = '''
{HL}#Flask app deploy config {EC}
       APP_NAME: {APP_NAME}
  DEPLOY_TARGET: {DEPLOY_TARGET}
      DEPLOY_ID: {CM}{DEPLOY_ID}{EC}

  DEPLOY_WWWROOT: {ER}{DEPLOY_WWWROOT}{EC}
     DEPLOY_PORT: {CM}{DEPLOY_PORT}{printedSSLCert}{EC}
     Apache site: {CM}{SITES_AVAILABLE}/{SITE_ID}.conf{EC}
   APP_LOG_ERROR: /var/log/apache2/{CM}{SITE_ID}.error.log{EC}
  APP_LOG_ACCESS: /var/log/apache2/{CM}{SITE_ID}.access.log{EC}
'''.format(
  HL=HL,CM=CM,EC=EC,ER=ER,

  APP_NAME=APP_NAME,
  DEPLOY_TARGET=DEPLOY_TARGET,
  DEPLOY_ID=DEPLOY_ID,

  DEPLOY_WWWROOT=DEPLOY_WWWROOT,
  DEPLOY_PORT=DEPLOY_PORT,
  printedSSLCert=printedSSLCert,
  SITES_AVAILABLE=SITES_AVAILABLE,
  SITE_ID=SITE_ID,
)

DEPLOYED_PUBLIC_PATHS = [
  p.replace(CODE_HOME, DEPLOY_WWWROOT) for p in APP_PUBLIC_PATHS
]

#endregion info printing