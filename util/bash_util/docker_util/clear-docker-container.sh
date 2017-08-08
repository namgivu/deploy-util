#!/usr/bin/env bash

docker rm -f $(docker ps -a -q) #ref. https://github.com/moby/moby/issues/23371#issuecomment-224927009