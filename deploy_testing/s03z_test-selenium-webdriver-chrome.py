#!/usr/bin/env python2.7
pass


#init Xvfb ref. https://stackoverflow.com/a/30103931/248616
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1024, 768))
display.start() #TODO ensure if we need to call display.close()


"""ref. http://www.seleniumhq.org/docs/03_webdriver.jsp#introducing-the-selenium-webdriver-api-by-example"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait #available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC #available since 2.26.0


##region webdriver option

#create options that be passed to the WebDriver initializer
options = webdriver.ChromeOptions()

#tell selenium to use the beta/dev channel version of chrome
options.binary_location = '/usr/bin/google-chrome-beta'

#set headless mode for chrome
options.add_argument('headless')

#set the window size
options.add_argument('window-size=1200x600')

#more options go here ref. https://sites.google.com/a/chromium.org/chromedriver/capabilities

##endregion webdriver option

#initialize the driver
driver = webdriver.Chrome(chrome_options=options)  #If nothing happens then everything worked! Normally, a new browser window would pop open at this point with a warning about being controlled by automated test software. It not appearing is exactly what we want to happen in headless mode and it means that we could be running our code on a server that doesn't even have a graphical environment. Everything from here on out is just standard Selenium so if you were only trying to figure out how to get it working with Chrome in headless mode then that's it!

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