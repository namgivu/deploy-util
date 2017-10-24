#!/usr/bin/env bash

: #ref. https://github.com/golang/go/wiki/Ubuntu

sudo add-apt-repository ppa:gophers/archive && \
  sudo apt update && \
  sudo apt install -y golang-1.9-go && \
  sudo apt autoremove -y
