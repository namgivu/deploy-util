#!/usr/bin/env bash

: #ref. https://www.rabbitmq.com/install-debian.html

#install prerequisite erlang/otp ref. https://stackoverflow.com/a/44690857/248616
cd "$HOME/Downloads" && \
  wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb && \
  sudo dpkg -i erlang-solutions_1.0_all.deb && \
  sudo apt update && sudo apt install -y esl-erlang=1:19.3.6 && \
cd --


#add the Apt repository to your Apt source list
echo "deb https://dl.bintray.com/rabbitmq/debian xenial main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list

#add rabbitmq public key to trusted key list
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -

#do install rabbitmq
sudo apt update && sudo apt install -y rabbitmq-server

#pinning erlang version #TODO consider using apt hold ref. https://askubuntu.com/a/18656/22308
sudo sh -c "
echo '
  Package: erlang*
  Pin: version 1:19.3-1
  Pin-Priority: 1000

  Package: esl-erlang
  Pin: version 1:19.3.6
  Pin-Priority: 1000
' >> /etc/apt/preferences" #pin file ref. https://help.ubuntu.com/community/PinningHowto
sudo apt-cache policy #check pinned package #TODO why this is not working i.e. 'Pinned packages:' line is empty

#aftermath check
sudo rabbitmqctl status

#stop/start reference
: sudo rabbitmqctl stop
: service rabbitmq-server start