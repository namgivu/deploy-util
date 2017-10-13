#!/usr/bin/env bash

#install java 8
sudo apt update
sudo apt-get install -y default-jdk

#config default java (optional) ref.https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04#managing-java
:: sudo update-alternatives --config java