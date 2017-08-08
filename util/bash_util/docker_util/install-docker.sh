#!/usr/bin/env bash

#applied for Ubuntu 16 only

#remove previous version if any
sudo apt-get remove docker docker-engine


##region set up apt repository
  #ref. https://docs.docker.com/engine/installation/linux/ubuntu/#set-up-the-repository

  sudo apt-get install -y \
      apt-transport-https \
      ca-certificates \
      curl \
      software-properties-common

  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo apt-key fingerprint 0EBFCD88
  sudo add-apt-repository \
     "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) \
     stable"
##endregion set up apt repository


#install docker (CE version)
sudo apt-get update
sudo apt-get install -y docker-ce


#aftermath check
sudo docker run hello-world
sudo docker --version


##region no sudo when use docker
  #ref. https://docs.docker.com/engine/installation/linux/linux-postinstall/#manage-docker-as-a-non-root-user

  #create user group docker and add current user to it
  sudo groupadd docker
  sudo usermod -aG docker $USER

  #prompt to log out and log in again
  echo "
    #Please log out and log in again!

    #After that, verify we can call docker without sudo as
    docker run hello-world
  "

##endregion no sudo when use docker
