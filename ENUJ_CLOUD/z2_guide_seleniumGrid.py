#!/usr/bin/env python2.7

#load config package
from config import *

#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options) #TODO Why passing --autorun=1 NOT working, while --verbose=1 works?
#endregion parse params


#region print infos & steps

infos=''


steps='''
{CM}#define input{EC}
export         SELENIUM_HUB='selenium-hub'
export            PORT_GRID='4443'
export SELENIUM_NODE_PREFIX='selenium-node'

export SELENIUM_HUB_STANDALONE_CH='selenium-hub-standalone-ch'
export         PORT_STANDALONE_CH='4444'
export SELENIUM_HUB_STANDALONE_FF='selenium-hub-standalone-ff'
export         PORT_STANDALONE_FF='4445'


{HL}#TODO add test for step s06_scale_selenium_grid.py {EC}
#TODO

{HL}#the grid{EC}
  {CM}#create the grid{EC}
  {ENUJ_CLOUD_HOME}/s05a_create_selenium_grid.py -h $SELENIUM_HUB -n $SELENIUM_NODE_PREFIX -p $PORT_GRID -a 1
  {CM}#delete the grid{EC}
  {ENUJ_CLOUD_HOME}/s05b_delete_selenium_grid.py -h $SELENIUM_HUB -n $SELENIUM_NODE_PREFIX -a 1
  
  {CM}#run a python selenium test{EC}
  {ER}#TODO grid method not working while standalone works, why?{EC}
  {ENUJ_CLOUD_HOME}/s05z_selenium_grid_test.py 
  
{HL}#the standalone{EC}
  {CM}#create standalone CHROME hub{EC}
  {ENUJ_CLOUD_HOME}/s05c_create_selenium_standalone.py -c $SELENIUM_HUB_STANDALONE_CH -p $PORT_STANDALONE_CH -b ch -a 1
  {CM}#delete standalone CHROME hub{EC}
  {ENUJ_CLOUD_HOME}/s03c_terminate_container.py -c $SELENIUM_HUB_STANDALONE_CH -a 1
  {CM}#run a python selenium test{EC}
  {ENUJ_CLOUD_HOME}/s05z_selenium_grid_test.py -b ch 

  {CM}#create standalone FIREFOX hub{EC}
  {ENUJ_CLOUD_HOME}/s05c_create_selenium_standalone.py -c $SELENIUM_HUB_STANDALONE_FF -p $PORT_STANDALONE_FF -b ff -a 1
  {CM}#delete standalone FIREFOX hub{EC}
  {ENUJ_CLOUD_HOME}/s03c_terminate_container.py -c $SELENIUM_HUB_STANDALONE_FF -a 1
  {CM}#run a python selenium test{EC}
  {ENUJ_CLOUD_HOME}/s05z_selenium_grid_test.py -b ff 
'''.format(
  ER=ER,HL=HL,CM=CM,EC=EC,
  ENUJ_CLOUD_HOME=ENUJ_CLOUD_HOME,
)

print(infos)

if not isAutorun: #print steps only when not autorun
  print(steps)

#endregion print infos & steps

if isAutorun: runPrintedSteps(
  steps, headline='Autorun %s' % os.path.basename(__file__)
)
