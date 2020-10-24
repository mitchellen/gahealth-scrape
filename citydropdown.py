'''
Run Script and pass a city in like './gahealth.py albany'
'''
import time
import sys
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
# #URL
URL = 'https://ga.healthinspections.us/stateofgeorgia/#home'
#CITY = sys.argv[1] # trying to make this obsolete and get them all
array = []
opts = Options()
opts.add_argument('--headless')
browser = Chrome(options=opts)
browser.get(URL)
time.sleep(4)
##Button Mashing##

select = Select(browser.find_element_by_id('city'))
cities = select.options
#remove the junk entry
cities.pop(0)
for c in cities:
    print(c.text)

#select.select_by_visible_text(CITY.upper())
#browser.find_element_by_id('searchButton').click()
