Deployment Utility
===

Intro
---

Deployment Utility helps us to deploy a Flask application to a Ubuntu Server machine hosted on amazon.com cloud.

Steps
---

- SSH connection to host
  + Goal<br> 
    Shortcut to open SSH-console to work with remote host from local machine
  
  + Input
    * HOST_IP
    * HOST_USER
    * HOST_PASS
    * HOST_SSH_KEY

- Upload files/utility-assets to host
  + Upload
    * deploy utility folder
    * git ssh key ie. git authentication via ssh key
    
  + With each upload entry
    * sourcePath
    * targetPath
