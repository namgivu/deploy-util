#!/usr/bin/env bash

#install PostgreSQL on Mac OS
#ref. https://gist.github.com/sgnl/609557ebacd3378f3b72

brew search postgres #there should be `postgresql`
brew install postgresql

: #follow the guide in the ref. above; steps as below
ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents

echo "
alias pg-start='launchctl load   ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist'
alias  pg-stop='launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist'
" >> ~/.profile

createdb "$USER"

#aftermath check
#ref. https://stackoverflow.com/a/13733884/248616
#ref. https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04
echo && which psql  && psql --version \
            && echo "
#connect postgres by
psql
psql -U $USER

#exit command (when inside psql prompt)
\q
"
