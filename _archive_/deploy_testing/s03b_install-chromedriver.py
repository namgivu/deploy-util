#!/usr/bin/env python2.7

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)
isAutorun = getArg('-a', options)
#endregion parse params


#region print infos & steps
steps='''
sudo echo 'sudo initiated'

{CM}#install prerequisites{EC}
#ref. https://stackoverflow.com/a/38689924/248616
#ref. apt-file search $MISSING_FILE
sudo apt install -y libglib2.0-0 
sudo apt install -y libnss3 
sudo apt install -y libx11-6 
sudo apt install -y libx11-6 
sudo apt install -y libfontconfig1

#ref. https://stackoverflow.com/a/23021454/248616
sudo apt-get install -y libxi6 libgconf-2-4

echo

{CM}#region download & unpack{EC}
  #install curl if require
  sudo apt-get install -y curl
  
  #do download
  echo "{eCM}#do download{eEC}"
  PLATFORM=linux64 #platform options: linux32, linux64, mac64, win32
  VERSION=$(curl -s http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
  DOWNLOAD_URL="http://chromedriver.storage.googleapis.com/$VERSION/chromedriver_$PLATFORM.zip"
  TMP_ZIP='/tmp/chromedriver.zip'
  curl $DOWNLOAD_URL > $TMP_ZIP
  echo

  #unpack using bsdtar ref. https://askubuntu.com/a/855993/22308
  echo "{eCM}#unpack using bsdtar{eEC}"
  sudo apt-get install -y bsdtar
  CHROMEDIRVER_HOME='/usr/local/share'
  sudo bsdtar -xvf $TMP_ZIP -C "$CHROMEDIRVER_HOME" #unzip using bsdtar ref. https://askubuntu.com/a/855993/22308
  echo

  #make chromedriver command globally available
  sudo ln -sf "$CHROMEDIRVER_HOME/chromedriver" /usr/local/bin/chromedriver
  sudo ln -sf "$CHROMEDIRVER_HOME/chromedriver" /usr/bin/chromedriver

{CM}#endregion download & unpack{EC}


{CM}#aftermath check{EC}
echo "
  {eCM}#Aftermath check{eEC}
  version `chromedriver --version`
  path    `which chromedriver`
"
'''.format(
  CM=CM,EC=EC,
  eCM=eCM,eEC=eEC,
  PIP_REQUIREMENT=PIP_REQUIREMENT,
)

print(steps)

#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
