import time
import dateutil.parser
import datetime
from selenium.common.exceptions import NoSuchElementException
from collections import deque
from checks.models import Check
import requests

NAME = 'SoulCycle'

STUDIO_BASE_URL = 'https://www.soul-cycle.com/find-a-class/studio/'
class Link:
  def __init__(self, url, date_string):
    self.url = url
    self.date_string = date_string

def check(driver, csv_writer):
    login(driver)
    time.sleep(2)
    locations = enumerate_locations(driver)
    for location in locations:
        print("checking " + location)
        check_location(driver, STUDIO_BASE_URL + locations.get(location), location, csv_writer, locations.get(location))

def enumerate_locations(driver):
    locations = {}
    studio_id = 1000
    consecutive_failures = 0
    while consecutive_failures < 10:  #currently under 2k so seems safe enough for now
        studio_url = "https://www.soul-cycle.com/find-a-class/studio/" + str(studio_id) + "/" # sick redirect on no trailing slash guyz
        result = requests.head(studio_url)
        studio_id += 1
        if (result.status_code == 302):
            driver.get(studio_url)
            try:
                location_name = driver.find_element_by_class_name('studio-title').text
                locations[location_name] = str(studio_id)
                consecutive_failures = 0
            except NoSuchElementException:
                consecutive_failures += 1
                pass  # sick consistent api responses guyz
    return locations

def check_location(driver, base_url, location, csv_writer, location_id):
  try:
    driver.get(base_url)
    links_to_visit = deque([Link(link.get_attribute('href'), link.get_attribute('data-class-time'))
        for link in driver.find_elements_by_class_name('reserve') 
        if dateutil.parser.parse(link.get_attribute('data-class-time')) >= datetime.datetime.now()])
    crawl(driver, links_to_visit, location, csv_writer, location_id)
  except Exception as e:
    print(NAME + ' done messed up on ' + location)
    print(e)

def login(driver):
  driver.get('https://www.soul-cycle.com/')
  link = driver.find_element_by_link_text('log in')
  link.click()
  username = driver.find_element_by_name("email")
  password = driver.find_element_by_name("password")

  username.send_keys("jimmadrigal@yopmail.com")
  password.send_keys("TestPassword1!")

  driver.find_element_by_name("submit").click()

def crawl(driver, links_to_visit, location, csv_writer, location_id):
  while len(links_to_visit) > 0:
    link_to_visit = links_to_visit.popleft()
    driver.get(link_to_visit.url)

    #on intercepted page from trying to sign up with no credits, skip
    try:
      driver.find_element_by_id('suggested-series-cancel').click()
    except NoSuchElementException:
      pass

    #if redirected to studio page with banner, parse
    try:
      banner_text = driver.find_element_by_id('confirmation-message-text').text
      if (banner_text == 'the class you requested is full! join the waitlist'):
        Check.objects.create(venue=NAME, location_id=location_id, location=location, slot_time=link_to_visit.date_string, is_full=True)
        csv_writer.writerow([datetime.datetime.now(), location, link_to_visit.date_string, '', '', 'true']) #TODO RMEMEBER TO USE NAME ("SoulCycle") IN PK
        continue
    except NoSuchElementException:
      pass

    #if on booking page, count open vs taken seats
    try:
      driver.find_element_by_class_name('location').text #todo should probs just regex the driver.current_url
      open_seats = len(driver.find_elements_by_css_selector('div.seat.open'))
      taken_seats = len(driver.find_elements_by_css_selector('div.seat.taken'))
      Check.objects.create(venue=NAME, location_id=location_id, location=location, slot_time=link_to_visit.date_string, open_seats = open_seats, taken_seats = taken_seats)
      csv_writer.writerow([datetime.datetime.now(), location, link_to_visit.date_string, str(open_seats), str(taken_seats), 'false']) #TODO RMEMEBER TO USE NAME ("SoulCycle") IN PK
    except NoSuchElementException:
      pass