'''
Run Script and pass a city in like './gahealth.py albany'
'''
import time
import sys
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import psycopg2
# db setup
# Set up Postgres database connection and cursor.
t_host = "localhost" # either "localhost", a domain name, or an IP address.
t_port = "5432" # default postgres port
t_dbname = "cityscrape"
t_user = "scrape"
t_pw = "password"
db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
db_conn.autocommit = True
db_cursor = db_conn.cursor()
if db_conn is not None:
    print('Connection established to PostgreSQL.')
else:
    print('Connection not established to PostgreSQL.')
# #URL
URL = 'https://ga.healthinspections.us/stateofgeorgia/#home'
CITY = sys.argv[1]
array = []
opts = Options()
#opts.add_argument('--headless')
browser = Chrome(options=opts)
browser.get(URL)
time.sleep(4)
##Button Mashing##
select = Select(browser.find_element_by_id('city'))
select.select_by_visible_text(CITY.upper())
browser.find_element_by_id('searchButton').click()
time.sleep(3)
#Scroll##
sel = browser.find_element_by_id('selection')
maybe = browser.find_element_by_xpath('//*[@id="wrapper"]/main/div')
for _ in range(100):
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", maybe)
    time.sleep(.5)

time.sleep(2)
titles = browser.find_elements_by_class_name("facility")
for t in titles:
    #print(t.text)
    l = t.find_elements_by_tag_name('li')
    name = l[0].text
    address = l[1].text
    phone = l[2].text.split(':')[1]
    permit = l[3].text.split(':')[1]
    score = l[4].text.split(':')[1]
    when = l[5].text.split(':')[1]
    postgres_insert_query = "INSERT INTO rest_scores (name,address,phone,permit,score,date) VALUES (%s,%s,%s,%s,%s,%s);"
    record_to_insert = (name,address,phone,permit,score,when,) # note the trailing comma
    # Trap errors for opening the file
    try:
        db_cursor.execute(postgres_insert_query, record_to_insert)
    except psycopg2.Error as e:
        print(e)
    # Success!
    sqlCreateTable = "create table rest_scores (name varchar(128),address text, phone varchar(128),permit varchar(128), score NUMERIC,date date NOT NULL);"
    #d = {'name': name, 'address': address, "phone": phone,\
         #"permit_type": permit, "score": score, "date":when}
    #array.append(d)
    ##
#df = pd.DataFrame(array)
#df = df.drop_duplicates(keep='last')
#print(df)
#df.to_csv("{}.csv".format(CITY.lower()), indbex=False)


browser.quit()
