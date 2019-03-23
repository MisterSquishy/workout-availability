import os
import time
import threading
import dateutil.parser
import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup, SoupStrainer
from collections import deque
import csv

chrome_bin = os.environ['GOOGLE_CHROME_SHIM']

STUDIO_BASE_URL = 'https://www.soul-cycle.com/find-a-class/studio/'
links_to_visit = deque([])
csv_writer_lock = threading.Lock()

class Link:
  def __init__(self, url, date_string):
    self.url = url
    self.date_string = date_string

def main(driver, base_url, location, csv_writer):
  driver.set_page_load_timeout(60)
  login(driver)
  time.sleep(2)

  driver.get(base_url)
  links_to_visit.extend([Link(link.get_attribute('href'), link.get_attribute('data-class-time'))
    for link in driver.find_elements_by_class_name('reserve') 
    if dateutil.parser.parse(link.get_attribute('data-class-time')) >= datetime.datetime.now()])
  

  while len(links_to_visit) > 0:
    link_to_visit = links_to_visit.popleft()
    driver.get(link_to_visit.url)

    #on intercepted page from trying to sign up with no credits , skip
    try:
      driver.find_element_by_id('suggested-series-cancel').click()
    except NoSuchElementException:
      pass

    #if redirected to studio page with banner, parse
    try:
      banner_text = driver.find_element_by_id('confirmation-message-text').text
      if (banner_text == 'the class you requested is full! join the waitlist'):
        with csv_writer_lock:
          csv_writer.writerow([datetime.datetime.now(), location, link_to_visit.date_string, '', '', 'true'])
        continue
    except NoSuchElementException:
      pass

    #if on booking page, count open vs taken seats
    try:
      driver.find_element_by_class_name('location').text #todo should probs just regex the driver.current_url
      open_seats = len(driver.find_elements_by_css_selector('div.seat.open'))
      taken_seats = len(driver.find_elements_by_css_selector('div.seat.taken'))
      with csv_writer_lock:
        csv_writer.writerow([datetime.datetime.now(), location, link_to_visit.date_string, str(open_seats), str(taken_seats), 'false'])
    except NoSuchElementException:
      pass

def login(driver):
  driver.get('https://www.soul-cycle.com/')
  link = driver.find_element_by_link_text('log in')
  link.click()
  username = driver.find_element_by_name("email")
  password = driver.find_element_by_name("password")

  username.send_keys("jimmadrigal@yopmail.com")
  password.send_keys("TestPassword1!")

  driver.find_element_by_name("submit").click()

def do_work(driver, base_url, location, csv_writer):
  try:
    main(driver, base_url, location, csv_writer)
  finally:
    driver.close()

DC_studio_ids = {
  '14th Street': '1041',
  'Georgetown': '1040',
  'Mount Vernon': '1037',
  'West End': '1013'
} 

with open('classes.csv', 'a') as csvfile:
  csv_writer = csv.writer(csvfile)
  threads = []
  for studio in DC_studio_ids:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location=chrome_bin
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.implicitly_wait(2)
    t = threading.Thread(target=do_work, args=(driver, STUDIO_BASE_URL + DC_studio_ids.get(studio), studio, csv_writer,))
    t.start()
    threads.append(t)
  [t.join() for t in threads] #await all threads to keep the file open