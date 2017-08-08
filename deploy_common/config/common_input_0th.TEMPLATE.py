#!/usr/bin/env python2.7

HOST_IP             = '#.##.###.#'
HOST_USER           = 'YOUR_HOST_USER'
HOST_PASS           = 'YOUR_HOST_PASS'
HOST_SSH_PORT       = 'YOUR_HOST_SSH_PORT' #leave empty to use default port 22

HOST_SSH_KEY        = '/path/to/YOUR_HOST_SSH_KEY/file' #use ssh key from local path eg. ~/.ssh/rbs-staging-ec2.pem ; when set will ignore HOST_SSH_KEY_URL
HOST_SSH_KEY_URL    = 'www.path.to/YOUR_HOST_SSH_KEY_URL/url' #use ssh key from a shared url; applied only when HOST_SSH_KEY is empty

HOST_DOCKERRSYNC_URL = 'rsync://{HOST_IP}:{RSYN_PORT}/some/path'.format(HOST_IP=HOST_IP) #leave empty if no docker-rsync url

APP_NAME            = 'YOUR_APP_NAME'
DEPLOY_TARGET       = 'YOUR_DEPLOY_TARGET' #e.g. LOCAL , STAGING , PRODUCTION , etc.
DEPLOY_ID           = '%s.%s' % (APP_NAME, DEPLOY_TARGET)
DEPLOY_PORT         = 'YOUR_PORT_HERE'
#SSL_CERT_FILE       = 'http://YOUR_SSL_CERT_FILE'    #when DEPLOY_PORT=443 only
#SSL_CERT_KEYFILE    = 'http://YOUR_SSL_CERT_KEYFILE' #when DEPLOY_PORT=443 only

CODE_GIT_REPO       = 'git@github.com:path_to/YOUR_CODE_GIT_REPO.git'
CODE_GIT_BRANCH     = 'YOUR_CODE_GIT_BRANCH'

CODE_GITHUB_KEY     = '/path/to/CODE_GITHUB_KEY/file' #use ssh key from local path eg. ~/.ssh/glassyteam-github-ssh; when set will ignore CODE_GITHUB_KEY_URL
CODE_GITHUB_KEY_URL = 'www.path.to/YOUR_HOST_SSH_KEY_URL/url' #use ssh key from a shared url; applied only when CODE_GITHUB_KEY is empty

PIP_REQUIREMENT     = None #None to use default pip 'requirements.txt' file; otherwise, put in a specific local path
