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


#region print infos & steps
infos='''
github SSH key info
CODE_GITHUB_KEY={CM}{printedCODE_GITHUB_KEY}{EC}
'''.format(
  HL=HL,CM=CM,EC=EC,
  printedCODE_GITHUB_KEY=CODE_GITHUB_KEY if CODE_GITHUB_KEY else CODE_GITHUB_KEY_URL,
)

##region build steps
steps=''

steps+='''#Adding github key... BEGIN
'''

#download github ssh key if needed
githubKey = CODE_GITHUB_KEY
if not CODE_GITHUB_KEY:
  githubKey = '%s/%s' % (REMOTE_SSH_HOME, DOWNLOAD_GITHUB_KEY)

#region step 1/2 add the key
sshConfig='%s/config' % REMOTE_SSH_HOME

steps += '''
{HL}#add github key to ssh agent{EC}
  echo "
  {eCM}#add github key to ssh agent{eEC}"
  
  {CM}#Start ssh agent {EC}
  eval $(ssh-agent -s)

  {CM}#Set up variables {EC}
  SSH_KEY={githubKey}

  {CM}#Add new ssh key {EC}
  chmod 600 $SSH_KEY
  ssh-add $SSH_KEY

  {CM}#Aftermath check {EC}
  echo 'list the added key'
  ssh-add -l
  echo


{HL}#tell git to use our github ssh key{EC}
  echo "
  {eCM}#tell github to use this specific key{eEC}"

  {CM}#do not append file {sshConfig} again if already exists{EC}
  #ref. https://stackoverflow.com/a/34716174/248616
  touch {sshConfig} #ensure file exists
  LINE_U="User         {CODE_GIT_REPO_USER}"
  LINE_I="IdentityFile $SSH_KEY"
  FOUND_U=`fgrep -c "$LINE_U" {sshConfig}`
  FOUND_I=`fgrep -c "$LINE_I" {sshConfig}`

  {CM}#write to file{EC}
  if [ "$FOUND_U" -eq "0" ] && [ "$FOUND_I" -eq "0" ]; then

    cat >> {sshConfig} << EOL
host {CODE_GIT_REPO_HOST}
  HostName     {CODE_GIT_REPO_HOST}
  User         {CODE_GIT_REPO_USER}
  IdentityFile $SSH_KEY
EOL
  
  fi

  {CM}#aftermath check{EC}
  g=`cat {sshConfig} | grep -i "$SSH_KEY"`
  echo "
  file : {sshConfig}
  grep : $g
"
  
'''.format(
  HL=HL, CM=CM, EC=EC, ER=ER,
  eHL=eHL, eCM=eCM, eEC=eEC, eER=eER,
  githubKey=githubKey,
  sshConfig=sshConfig,
  CODE_GIT_REPO_HOST=CODE_GIT_REPO_HOST,
  CODE_GIT_REPO_USER=CODE_GIT_REPO_USER,
)

#endregion step 1/2 add the key


#region step 2/2 reload ssh key when logged-in
githubKeyInBash=githubKey.replace(REMOTE_HOME, REMOTE_HOME_bash)
bashrc_codes= '''

#region reload github ssh key when logged-in
  eval \\$(ssh-agent -s)
  key="{githubKeyInBash}"
  ssh-add \$key
  echo -e \"{eCM}Github SSH key loaded at '\$key' {eEC} \"
  echo
#endregion

'''.strip()\
   .format(eCM=eCM,eEC=eEC,
           githubKeyInBash=githubKeyInBash,
           )


steps += '''
{HL}#load ssh key on login{EC}
  echo "
  {eCM}#load ssh key on login{eEC}"

  {CM}#do not append file {BASHRC} again if already exists{EC}
  #ref. https://stackoverflow.com/a/34716174/248616
  touch {BASHRC} #ensure file exists
  LINE_K="key=\\"{githubKeyInBash}\\""
  FOUND_K=`fgrep -c "$LINE_K" {BASHRC}`

  {CM}#write to file{EC}
  if [ "$FOUND_K" -eq "0" ]; then
  
    cat >> {BASHRC} << EOL
{bashrc_codes}
EOL

  fi

  {CM}#aftermath check{EC}
  echo "
  file : {BASHRC}
  grep : `cat {BASHRC} | grep -i '{githubKeyInBash}'`
"
'''.format(
  HL=HL, CM=CM, EC=EC, ER=ER,
  eHL=eHL, eCM=eCM, eEC=eEC, eER=eER,
  BASHRC=BASHRC,
  bashrc_codes=bashrc_codes,
  githubKeyInBash=githubKeyInBash,
)

#endregion step 2/2 reload ssh key when logged-in


#region ending
steps += '''
{HL}#restart remind{EC}
  echo 
  echo 'Github ssh key installed - {eER}please RE-CONNECT ssh console !{eEC}'
  echo 'After reconnected, fetch a github connection by {eER}ssh -T {CODE_GIT_REPO_USER}@{CODE_GIT_REPO_HOST}{eEC}'

#Adding github key... END
'''.format(
  HL=HL,CM=CM,EC=EC,
  eHL=eHL,eCM=eCM,eER=eER,eEC=eEC,
  CODE_GIT_REPO_USER=CODE_GIT_REPO_USER,
  CODE_GIT_REPO_HOST=CODE_GIT_REPO_HOST,
)
#endregion ending


##region build steps
print(infos)

if not isAutorun:
  print(steps)
#endregion print infos & steps


#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
