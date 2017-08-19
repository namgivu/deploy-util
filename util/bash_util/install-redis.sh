#!/usr/bin/env bash

#ref. https://askubuntu.com/a/868953/22308

#install
sudo apt install redis-server

#region aftermath check

echo "
  #start redis service:
  sudo systemctl start redis

  #check status
  systemctl status redis

  #region check the instance
    #connect
    redis-cli

    #test connectivity at prompt
    ping   #result pong

    #check ability to set keys
    set test 122  #result ok

    #check get the key just set
    get test  #result 122

    #exit redis
    exit
  #endregion check the instance


  #auto start when boot
  sudo systemctl enable redis
"

#endregion aftermath check
