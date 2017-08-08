#!/usr/bin/env python2.7
pass

# HOST_IP             = '192.168.1.113'
HOST_IP             = 'localhost'
HOST_USER           = 'seluser'
HOST_PASS           = ''
HOST_SSH_PORT       = '22000' #leave empty to use default port 22

HOST_SSH_KEY        = '' #use ssh key from local path eg. ~/.ssh/YOUR-KEY.pem ; when set will ignore HOST_SSH_KEY_URL

#HOST_SSH_KEY_URL = 'http://192.168.1.113//html/enuj.113/docker-ssh_22000_autotest_a8d421' #use ssh key from a shared url; applied only when HOST_SSH_KEY is empty
HOST_SSH_KEY_URL = 'http://{HOST_IP}/enuj.113/docker-ssh_22000_autotest_447199'.format(HOST_IP=HOST_IP)

HOST_RSYNC_PORT      = '18000' #port to rsync against ENUJ host
HOST_DOCKERRSYNC_URL = 'rsync://{HOST_IP}:{HOST_RSYNC_PORT}/volume'.format(HOST_IP=HOST_IP, HOST_RSYNC_PORT=HOST_RSYNC_PORT) #leave empty if no docker-rsync url

DEPLOY_HOME_PREFIX  = 'autotest' #left empty to set as 'deploy'
APP_NAME            = 'YOUR_APP'
DEPLOY_TARGET       = 'ENUJ' #e.g. LOCAL , STAGING , PRODUCTION , etc.
DEPLOY_ID           = '%s.%s' % (APP_NAME, DEPLOY_TARGET)
DEPLOY_PORT         = None #test run from command line only

CODE_GIT_REPO       = 'git@github.com:duyhtq/automation_testing.git'
CODE_GIT_BRANCH     = 'master'

CODE_GITHUB_KEY     = '' #use ssh key from local path eg. ~/.ssh/glassyteam-github-ssh; when set will ignore CODE_GITHUB_KEY_URL
CODE_GITHUB_KEY_URL = 'http://URL.to-your-key.com' #use ssh key from a shared url; applied only when CODE_GITHUB_KEY is empty

PIP_REQUIREMENT     = None #None to use default pip 'requirements.txt' file; otherwise, put in the req. file path

UTIL_PRUNED_LIST    = 'deploy_brain:deploy_flask:deploy_mysql:ENUJ_CLOUD:venv' #list of pruned file/folder; separated by colon : e.g. 'deploy_brain:deploy_mysql' or left empty to remove nothing
