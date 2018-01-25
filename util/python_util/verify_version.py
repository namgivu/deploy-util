#!/usr/bin/env python
from .misc import *


def verify_version(name):
  name=name.lower()

  if False: pass

  elif name in ['os', 'ubuntu', 'centos', 'amazon-linux', 'linux']:
    run_bash('cat /etc/os-release | grep PRETTY_NAME')

  #region python
  elif name in ['python']:
    run_bash('which python ; python -V')

  elif name in ['virtualenv', 'venv']:
    run_bash('which virtualenv; virtualenv --version')

  elif name in ['pip']:
    run_bash('which pip; pip --version')

  elif name in ['flask']:
    run_bash('pip freeze | grep Flask==')
  #endregion python

  elif name in ['mysql']:
    run_bash('which mysql ; mysql -V')

  elif name in ['apache', 'apache2']:
    run_bash("which apache2 ; apachectl -v | grep 'Server version' ")

  elif name in ['apache-wsgi', 'wsgi']:
    run_bash("dpkg -l | grep wsgi")

  elif name in ['aws', 'awscli', 'aws-cli', 'aws-eb', 'aws-s3']:
    run_bash("aws --version")

  elif name in ['go']:
    run_bash("go version")

  else:
    raise Exception(
      '{ER}Invalid software name "{name}" {EC}'.format(ER=ER, name=name, EC=EC)
    )

  pass


if __name__=='__main__': #this file is executed ref. http://stackoverflow.com/a/419185/248616
  """
  This program take in 1st command-line argument as `name` as software name
  and then print the version of it
  """

  #region get name param
  import sys ; argv = sys.argv[1:]
  try:    name=argv[0]
  except: name=None
  #endregion get name param

  if name: verify_version(name)