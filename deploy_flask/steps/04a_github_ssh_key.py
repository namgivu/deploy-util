#!/usr/bin/env python2.7

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
infos='''
{HL}Configure github SSH key {EC}
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
  {HL}#add github key to ssh agent BEGIN {EC}
    {CM}#Set up variables {EC}
    export SSH_KEY={githubKey}

    {CM}#Start ssh agent {EC}
    eval $(ssh-agent -s)

    {CM}#Add new ssh key {EC}
    chmod 600 $SSH_KEY
    ssh-add $SSH_KEY

    {CM}#Aftermath check {EC}
    echo ''
    ssh-add -l

  {HL}#add github key to ssh agent END {EC}


  {ER}#TODO DON'T append setting lines again if already exists{EC}
  {HL}#tell github to use this specific key BEGIN {EC}
  cat >> {sshConfig} << EOL
host github.com
  HostName     {CODE_GIT_REPO_HOST}
  User         {CODE_GIT_REPO_USER}
  IdentityFile $SSH_KEY
EOL
  {HL}#tell github to use this specific key END {EC}
'''.format(
  HL=HL, CM=CM, EC=EC, ER=ER,
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


#TODO DON'T append setting lines again if already exists
steps += '''
  {HL}#reload key on log-in BEGIN {EC}
  cat >> {BASHRC} << EOL
{bashrc_codes}
EOL
  {HL}#reload key on log-in END {EC}
'''.format(
  HL=HL, CM=CM, EC=EC, ER=ER,
  BASHRC=BASHRC,
  bashrc_codes=bashrc_codes,
)

#endregion step 2/2 reload ssh key when logged-in

#region ending
steps += '''
  {HL}#aftermath check {EC}
  echo; echo '{eHL}Aftermath check{eEC}'
    
    echo '{eCM}#In {BASHRC} where our github key loaded{eEC}'
    cat {BASHRC} | grep -i '{githubKeyInBash}'
    
    echo
    
    echo '{eCM}#In {sshConfig} where git is set up to used our key{eEC}'
    cat {sshConfig} | grep -i '{DEPLOY_ID}'

  {HL}#restart remind{EC}
  echo; 
  echo 'Github ssh key installed - {eER}please RE-CONNECT ssh console !{eEC}'
  echo 'After reconnected, fetch a github connection by {eER}ssh -T {CODE_GIT_REPO_USER}@{CODE_GIT_REPO_HOST}{eEC}'
'''.format(
  HL=HL,CM=CM,EC=EC,
  eHL=eHL,eCM=eCM,eER=eER,eEC=eEC,
  BASHRC=BASHRC,
  githubKey=githubKey,
  sshConfig=sshConfig,
  githubKeyInBash=githubKeyInBash,
  DEPLOY_ID=DEPLOY_ID,
  CODE_GIT_REPO_USER=CODE_GIT_REPO_USER,
  CODE_GIT_REPO_HOST=CODE_GIT_REPO_HOST,
)
#endregion ending

steps+='''

#Adding github key... END'''

##endregion build steps

print(infos)
print(steps)

pass
#endregion print infos & steps


#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun configuring github ssh key'
)
