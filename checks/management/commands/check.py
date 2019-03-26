from django.core.management.base import BaseCommand
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
from venues import venues

class Command(BaseCommand):
    def handle(self, **options):
        chrome_bin = os.environ['GOOGLE_CHROME_SHIM']
        with open(os.getcwd() + '/classes.csv', 'a') as csvfile:
            csv_writer = csv.writer(csvfile)
            for venue in venues:
                try:
                    options = webdriver.ChromeOptions()
                    options.add_argument('headless')
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                    options.binary_location=chrome_bin
                    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
                    driver.implicitly_wait(5)
                    driver.set_page_load_timeout(60)
                    venue.check(driver, csv_writer)
                except Exception as e:
                    print("I done messed up on " + venue.NAME)
                    print(e)
                finally:
                    driver.close()
        driver.quit()