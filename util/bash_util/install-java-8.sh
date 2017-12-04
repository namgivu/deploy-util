#!/usr/bin/env bash

: #ref. https://stackoverflow.com/a/14788468/248616
: #ref. https://askubuntu.com/a/755854/22308

#install java 8
sudo apt update
sudo apt install -y openjdk-8-jdk
sudo apt install -y openjdk-8-source #this is optional, the jdk source code - you may need this to understand jdk lib's function param/meaning

#region config java (optional)

  #config default java version ref. https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04#managing-java
  : sudo update-alternatives --config java

  #config java e.g. JAVA_HOME ref. https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04#setting-the-java_home-environment-variable
  ls -la `which java`           #get /usr/bin/java -> /etc/alternatives/java
  ls -la /etc/alternatives/java #get /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -> JAVA_HOME='/usr/lib/jvm/java-8-openjdk-amd64'
  : sudo nano /etc/environment  #set JAVA_HOME="/usr/PATH/TO/YOUR/JDK" e.g. JAVA_HOME='/usr/lib/jvm/java-8-openjdk-amd64'
  : nano $HOME/.bashrc #add line `source /etc/environment` ref. https://askubuntu.com/a/175547/22308

#endregion

#aftermath check
echo ; java -version