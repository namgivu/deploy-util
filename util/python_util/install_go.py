#!/usr/bin/env python

from .common import * #initiate common asset

USER_HOME = '~'
GOPATH    = '%s/gows' % USER_HOME
USR_LOCAL = '/usr/local'
BASHRC    = '~/.bashrc'

steps='''
#Commands to download & install Go

{HL}#Init sudo{EC}
  sudo echo 'sudo initiated';

{HL}#Get prepared{EC}
     BASHRC='{BASHRC}'
      goPkg='go1.8.3.linux-amd64' #latest version ref. https://golang.org/dl/#stable
  USR_LOCAL='{USR_LOCAL}'
     GOPATH='{GOPATH}'

{HL}#Download and unpack Go{EC}
  {CM}#do download{EC}
  wget https://storage.googleapis.com/golang/$goPkg.tar.gz

  {CM}#do unpack{EC}
  sudo -H tar -C $USR_LOCAL -xzf $goPkg.tar.gz

{HL}#Add 'go' command to system PATH{EC}

  #do adding
  cat << EOF >> $BASHRC

#Add 'go' command to system PATH
export PATH="$USR_LOCAL/go/bin:\$PATH"
EOF

  #aftermath check
  source $BASHRC
  echo
  which go
  go version

{HL}#Create environment variable GOPATH{EC}
  mkdir -p $GOPATH

  {CM}#register path via .bashrc {EC}
  sudo cat >> $BASHRC <<EOL

#variable GOPATH and its binary
export GOPATH=$GOPATH
export PATH="\$GOPATH/bin:\$PATH"
EOL

  {CM}#reload .bashrc {EC}
  source $BASHRC
  echo GOPATH=$GOPATH
'''.format(
  HL=HL,CM=CM,EC=EC,
  BASHRC=BASHRC,
  GOPATH=GOPATH,
  USR_LOCAL=USR_LOCAL,
  USER_HOME=USER_HOME,
)

steps+='''
{HL}#Aftermath check{EC}
  {CM}#(optional) reconnect your SSH session{EC}

  {CM}#print go version & path{EC}
  echo 'go binary'
  which go
  go version

  echo
  echo "GOPATH=$GOPATH"

  {CM}#run a go code file{EC}
  echo 'Test code'

  #code a file hello.go ref. https://golang.org/doc/install#testing
  testGo='testGo'
  testGoSrc="$GOPATH/src/$testGo" ; mkdir -p $testGoSrc

  hello="$testGoSrc/hello.go"
  cat > $hello <<EOL
package main

import "fmt"

func main() {{
  fmt.Printf("hello, world\\n")
}}
EOL

  #install code
  go install $testGo

  echo ; echo 'Run code'
  $GOPATH/bin/$testGo
'''.format(
  HL=HL,CM=CM,EC=EC,
)

print(steps)
