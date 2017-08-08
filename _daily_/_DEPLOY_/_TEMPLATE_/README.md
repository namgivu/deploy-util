This folder contains all utilities shared among different distro deployment eg. STAGING, PRODUCTION, etc

Please create symlink to those utilities for your distro folder. 

You may find `create-symlink.sh` useful
- create link
  ./create-symlink.sh /path/to/distro/folder 
- rollback created link
  ./create-symlink.sh /path/to/distro/folder rollback 
