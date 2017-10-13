#!/usr/bin/env bash

#install java 8
sudo apt update
sudo apt-get install -y default-jdk

#region config java (optional)

  #config default java version ref. https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04#managing-java
  :: sudo update-alternatives --config java

  #config java e.g. JAVA_HOME ref. https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04#setting-the-java_home-environment-variable
  :: sudo nano /etc/environment #set JAVA_HOME="/usr/PATH/TO/YOUR/JDK"

#endregion