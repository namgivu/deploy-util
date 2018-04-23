HOME_PAGE_URL='http://ec2-54-208-76-28.compute-1.amazonaws.com' #STAGING aos web
HOME_PAGE_TITLE='Autonomous: Smart Office. Work Smarter. Be Healthier. Be More Productive.'

#list of test vault packages to run
"""Comment on/off below lines to add/omit test in the corresponding package"""
TEST_VAULT_PACKAGE=[
  'aos_web',
]


#region SNAPSHOT_DEBUG=TRUE/False means DO/don't take snapshot during the run
SNAPSHOT_DEBUG = True
#endregion


#region ENABLED_TEST=TRUE/False means DO/don't enable all tests
# ENABLED_TEST = False
#endregion


#region webdriver config i.e. to use local/remote webdriver
pass

# WEBDRIVER_REMOTE_HUB = '' #left empty to use local

WEBDRIVER_REMOTE_HUB = 'http://localhost:4444/wd/hub' #4444 the hub-node grid
# WEBDRIVER_REMOTE_HUB = 'http://localhost:4446/wd/hub' #4446 the standalone firefox hub
# WEBDRIVER_REMOTE_HUB = 'http://localhost:4445/wd/hub' #4445 the standalone chrome hub

# WEBDRIVER_REMOTE_HUB = 'http://192.168.1.113:4444/wd/hub' #ENUJ:4444 the hub-node grid on ENUJ
# WEBDRIVER_REMOTE_HUB = 'http://13.229.8.218:4444/wd/hub' #LS:4444 the hub-node grid on AWS LS #NOTE: we SHOULD NOT run this way due to 0) network I/O cost by AWS, 1) slow connection

pass
#endregion
