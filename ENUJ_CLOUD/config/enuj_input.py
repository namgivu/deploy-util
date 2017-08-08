#!/usr/bin/env python2.7
from . import UTILITY_ROOT
import os

#common home path
ENUJ_CLOUD_HOME     = os.path.abspath('%s/ENUJ_CLOUD' % UTILITY_ROOT)
DOCKER_BASH_UTIL    = os.path.abspath('%s/util/bash_util/docker_util' % UTILITY_ROOT)
BASH_UTIL           = os.path.abspath('%s/util/bash_util' % UTILITY_ROOT)
ENUJ_VAULT          = os.path.abspath('%s/_vault_'         % ENUJ_CLOUD_HOME)
ENUJ_SSH_KEY_VAULT  = os.path.abspath('%s/_vault_/ssh_key' % ENUJ_CLOUD_HOME)

ENUJ_PUBLISHED_FOLDER = 'enuj.113'
ENUJ_PUBLISHED_SUBPATH = '/html/%s' % ENUJ_PUBLISHED_FOLDER
ENUJ_SSH_KEY_PUBLISHED_VAULT = '/var/www/html/%s' % ENUJ_PUBLISHED_FOLDER

ENUJ_PHYSICAL_IP = '192.168.1.113'

##region docker image w/ its $USER, $HOME
pass


class EnujDockerImage:
  def __init__(self): pass

  #UBUNTU = 'ubuntu' #latest ubuntu but unsure what version
  UBUNTU_1604 = 'ubuntu:16.04'  # ref. https://hub.docker.com/_/ubuntu/

  DOCKER_SELENIUM_HUB   = 'selenium/standalone-chrome:3.4.0-einsteinium' #ref. https://github.com/SeleniumHQ/docker-selenium#running-the-images #TODO remove this since we don't need ssh/rsync to this image
  DOCKER_SELENIUM_NODE  = 'TODO'
  DOCKER_FLASK_HOSTING  = 'TODO'
  DOCKER_MYSQL_HOSTING  = 'TODO'


ContainerUser = dict()
ContainerUser[EnujDockerImage.UBUNTU_1604]          = 'root'
ContainerUser[EnujDockerImage.DOCKER_SELENIUM_HUB]  = 'seluser'
ContainerUser[EnujDockerImage.DOCKER_SELENIUM_NODE] = 'TODO'


ContainerUserHome = dict()
ContainerUserHome[EnujDockerImage.UBUNTU_1604]          = '/root'
ContainerUserHome[EnujDockerImage.DOCKER_SELENIUM_HUB]  = '/home/seluser'
ContainerUserHome[EnujDockerImage.DOCKER_SELENIUM_NODE] = 'TODO'

pass
##region docker image w/ its $USER, $HOME


#region load local input
try: from enuj_input_local import *
except: pass
#endregion
