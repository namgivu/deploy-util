#!/usr/bin/env python2.7
pass

#load config package
from config import *


#region parse params
options = dict(
  shortOpts = 'b:',
  longOpts  = ['browser='],
)

BROWSER = getArg('-b', options)

"""ref. http://www.seleniumhq.org/docs/03_webdriver.jsp#introducing-the-selenium-webdriver-api-by-example"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait #available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC #available since 2.26.0


def runTest(driver):
  #go to the google home page
  driver.get('http://www.google.com')


  #the page is ajaxy so the title is originally this:
  print(driver.title)

  #find the element that's name attribute is q (the google search box)
  inputElement = driver.find_element_by_name('q')

  #type in the search
  inputElement.send_keys('cheese!')

  #submit the form (although google automatically searches now without submitting)
  inputElement.submit()

  try:
    #we have to wait for the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(driver, 10).until(EC.title_contains('cheese!'))

    #You should see 'cheese! - Google Search'
    print(driver.title)

  finally:
    driver.quit()


REMOTE_WEB_DRIVER_HUB            = 'http://localhost:4443/wd/hub'
REMOTE_WEB_DRIVER_STANDALONE_ch  = 'http://localhost:4444/wd/hub'
REMOTE_WEB_DRIVER_STANDALONE_ff  = 'http://localhost:4445/wd/hub'


from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

if False: pass

elif BROWSER=='ch':
  ##region run test #1 chrome
  pass

  #create options that be passed to the WebDriver initializer
  options = webdriver.ChromeOptions()
  options.add_argument('headless')
  options.add_argument('window-size=1200x600')

  #initialize the driver for REMOTE webdriver
  desired_capabilities=options.to_capabilities()

  #TODO why this is not working?

  #run test
  # driver01 = webdriver.Remote(
  #   command_executor=REMOTE_WEB_DRIVER,
  #   desired_capabilities=options.to_capabilities(),
  # )
  # runTest(driver01)

  pass
  ##endregion run test #1


  ##region run test #2 chrome
  pass

  command_executor = REMOTE_WEB_DRIVER_STANDALONE_ch
  driver02 = webdriver.Remote(
    command_executor=command_executor,
    desired_capabilities=DesiredCapabilities.CHROME,
  )
  print('Running test against %s' % command_executor)
  runTest(driver02)

  pass
  ##endregion run test #2


elif BROWSER=='ff':
  ##region run test #3 firefox
  pass

  command_executor = REMOTE_WEB_DRIVER_STANDALONE_ff
  driver03 = webdriver.Remote(
    command_executor=command_executor,
    desired_capabilities=DesiredCapabilities.FIREFOX,
  )
  print('Running test against %s' % command_executor)
  runTest(driver03)

  pass
  ##endregion run test #2

else: #no browser specified, run on the hub
  command_executor = REMOTE_WEB_DRIVER_HUB
  print('Running test against GRID %s' % command_executor)

  # print('\nBrowser=ch')
  # driverCH = webdriver.Remote(
  #   command_executor=command_executor,
  #   desired_capabilities=DesiredCapabilities.CHROME,
  # )
  # runTest(driverCH)

  print('\nBrowser=ff')
  driverFF = webdriver.Remote(
    command_executor=command_executor,
    desired_capabilities=DesiredCapabilities.FIREFOX,
  )
  runTest(driverFF)
