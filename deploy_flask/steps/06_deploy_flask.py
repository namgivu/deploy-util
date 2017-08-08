#!/usr/bin/env python2.7

#TODO support deploy duo port http/https ie. 80/443

from common import * #initiate common asset
from input  import * #load the inputs

#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options)
#endregion parse params


#region print infos & steps

##region info
infos = FLASK_DEPLOY_INFO
##endregion info

##region build steps
steps='''
#Steps to deploy flask app as apache wsgi app BEGIN
'''

##region Make config

#region make Apache site config
steps+='''
  {HL}#Make Apache site config {EC}
  echo 'Make Apache site config...'
'''.format(HL=HL,CM=CM,EC=EC,ER=ER,)

steps += '''
  {CM}#init sudo{EC}
  sudo echo 'sudo initiated'
  
  {CM}#clone config files from templates {EC}
  rm -rf {SITE_CONFIG_GEN} ; mkdir -p {SITE_CONFIG_GEN};
  rsync -chaz {SITE_CONFIG_TEMPLATE}/ {SITE_CONFIG_GEN}/
  sudo locale-gen 'vi_VN.UTF-8' > /dev/null #install locale to use rename/perl ref. http://stackoverflow.com/a/9727654
  {pushd} && cd {SITE_CONFIG_GEN} && rename -f 's/^/{DEPLOY_ID}./g' * && {popd} #adding prefix DEPLOY_ID to files
'''.format(
  HL=HL,CM=CM,EC=EC,ER=ER,

  SITE_CONFIG_GEN=SITE_CONFIG_GEN,
  SITE_CONFIG_TEMPLATE=SITE_CONFIG_TEMPLATE,
  DEPLOY_ID=DEPLOY_ID,

  #pushd & popd without output ref. http://serverfault.com/a/108160/41015
  pushd='curDir=`pwd`',
  popd='cd $curDir',
)

siteConf_MASTER = '{SITE_CONFIG_GEN}/{DEPLOY_ID}.{SITECONF_MASTER}'.format(
  SITE_CONFIG_GEN=SITE_CONFIG_GEN,
  DEPLOY_ID=DEPLOY_ID,
  SITECONF_MASTER=SITECONF_MASTER,
)
siteConf_SUB00 = '{SITE_CONFIG_GEN}/{DEPLOY_ID}.{SITECONF_SUB00}'.format(
  SITE_CONFIG_GEN=SITE_CONFIG_GEN,
  DEPLOY_ID=DEPLOY_ID,
  SITECONF_SUB00=SITECONF_SUB00,
)
steps+='''
  {CM}#fill in config files with app infos {EC}
  export siteConf="{siteConf_MASTER}"
  key='DEPLOY_ID'       && sed -i -e "s|Define[ ]*$key.*|Define $key {DEPLOY_ID}|g" $siteConf
  key='SITES_AVAILABLE' && sed -i -e "s|Define[ ]*$key.*|Define $key {SITES_AVAILABLE}|g" $siteConf
  :
  export siteConf="{siteConf_SUB00}"
  key='DEPLOY_ID'       && sed -i -e "s|Define[ ]*$key.*|Define $key {DEPLOY_ID}|g" $siteConf
  key='DEPLOY_WWWROOT'  && sed -i -e "s|Define[ ]*$key.*|Define $key {DEPLOY_WWWROOT}|g" $siteConf
  key='DEPLOY_PORT'     && sed -i -e "s|Define[ ]*$key.*|Define $key {DEPLOY_PORT}|g" $siteConf
  key='ServerAdmin'     && sed -i -e "s|Define[ ]*$key.*|Define $key {ServerAdmin}|g" $siteConf
'''.format(
  HL=HL,CM=CM,EC=EC,ER=ER,

  siteConf_MASTER=siteConf_MASTER,
  siteConf_SUB00=siteConf_SUB00,

  DEPLOY_ID=DEPLOY_ID,
  SITES_AVAILABLE=SITES_AVAILABLE,
  DEPLOY_WWWROOT=DEPLOY_WWWROOT,
  DEPLOY_PORT=DEPLOY_PORT,
  ServerAdmin=ServerAdmin,
)

if isSSL(DEPLOY_PORT): #ssl/https protocol is required => turn them on in site config
  steps+='''
  {CM}#turn on ssl config {EC}
  sudo echo 'sudo initiated' #init sudo
  :
  export certFile='{REMOTE_CERT_FILE}'
  export certKey='{REMOTE_CERT_KEY}'
  sudo mkdir -p {REMOTE_SSL_HOME}
  sudo wget -q -O $certFile    {SSL_CERT_FILE}    ; ls -l $certFile
  sudo wget -q -O $certKey {SSL_CERT_KEYFILE} ; ls -l $certKey
  :
  export siteConf="{siteConf_MASTER}"
  sed -i -e "s|#SSLEngine.*|SSLEngine on|g" $siteConf
  sed -i -e "s|#SSLCertificateFile.*|SSLCertificateFile $certFile|g" $siteConf
  sed -i -e "s|#SSLCertificateKeyFile.*|SSLCertificateKeyFile $certKey|g" $siteConf
  :'''.format(
    HL=HL,CM=CM,EC=EC,ER=ER,
    REMOTE_CERT_FILE=REMOTE_CERT_FILE,
    REMOTE_CERT_KEY=REMOTE_CERT_KEY,
    REMOTE_SSL_HOME=REMOTE_SSL_HOME,
    DEPLOY_ID=DEPLOY_ID,
    SSL_CERT_FILE=SSL_CERT_FILE,
    SSL_CERT_KEYFILE=SSL_CERT_KEYFILE,
    siteConf_MASTER=siteConf_MASTER,
  )
#endregion make Apache site config

#region make Flask local config
steps += '''
  {HL}#Make local Flask config {EC}
  echo 'Make local Flask config...'
  cp -f {RBS_LOCAL_CONFIG_TEMPLATE} {RBS_LOCAL_CONFIG}
'''.format(
  HL=HL,CM=CM,EC=EC,

  RBS_LOCAL_CONFIG_TEMPLATE=RBS_LOCAL_CONFIG_TEMPLATE,
  RBS_LOCAL_CONFIG=RBS_LOCAL_CONFIG,
)
#endregion make local config

##endregion Make config

#region prepare code at wwwroot
steps+='''
  echo 'Prepare code at wwwroot...'

  {HL}#Copy code to web root {EC}
  sudo rm -rf {DEPLOY_WWWROOT}
  sudo mkdir -p {DEPLOY_WWWROOT}
  sudo rsync -chaz  --exclude .git  {APP_CODE}/ {DEPLOY_WWWROOT}/ {CM}#exclude .git folder ref. http://www.thegeekstuff.com/2011/01/rsync-exclude-files-and-folders/?utm_source=feedburner{EC}

  {HL}#Authorize permission for www-data on public paths {EC}
    {CM}#chown i.e. set owner{EC}
    sudo chown -R www-data:www-data {printedAPP_PUBLIC_PATHS}

    {CM}#chmod i.e. set file permission{EC}
    sudo chmod -R 777 {printedAPP_PUBLIC_PATHS}
'''.format(
  HL=HL,CM=CM,EC=EC,
  DEPLOY_WWWROOT=DEPLOY_WWWROOT,
  APP_CODE=APP_CODE,
  printedAPP_PUBLIC_PATHS=' '.join(APP_PUBLIC_PATHS),
)
#endregion prepare code at wwwroot

#region site register with apache
steps+='''
  echo 'Site register with apache...'

  sudo echo 'sudo initiated' #init sudo

  {HL}#Turn off default apache site on port 80 {EC}
  sudo a2dissite 000-default.conf {silentOutput} && sudo service apache2 reload

  {HL}#TODO Turn off any other apache site on port 80 {EC}

  {HL}#Un-register current hosted site if any{EC}
  sudo a2dissite {SITE_ID} {silentOutput} && sudo service apache2 reload

  {HL}#Register site {EC}
    {CM}#site config files {EC}
    sudo rsync -chaz {SITE_CONFIG_GEN}/ {SITES_AVAILABLE}/

    {CM}#do register {EC}
    sudo a2ensite {SITE_ID} -q {silentOutput}

  {HL}#Reload apache {EC}
  sudo service apache2 --full-restart #TODO why not this simple call `sudo service apache2 reload` ?

#Steps to deploy flask app as apache wsgi app END
'''.format(
  HL=HL,CM=CM,EC=EC,
  SITE_CONFIG_GEN=SITE_CONFIG_GEN,
  SITES_AVAILABLE=SITES_AVAILABLE,
  SITE_ID=SITE_ID,

  #silentOutput='> /dev/null',
  silentOutput='',
)
#endregion site register with apache

##endregion build steps

print(infos)
print(steps)
#endregion print infos & steps


#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun deploying flask app'
)
