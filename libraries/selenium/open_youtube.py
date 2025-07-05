from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

chrome_path = "chrome-linux64/chrome"
driver_path = "chromedriver-linux64/chromedriver"

options = Options()
options.binary_location = chrome_path
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless")  # headless mode
options.add_argument("--window-size=1280,1024")  # Set size for full screenshot


service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.youtube.com")
time.sleep(2)


search_box = driver.find_element(By.NAME, "search_query")


search_box.send_keys("lofi music")
search_box.submit()

time.sleep(3)
print("Search Result Page Title:", driver.title)
driver.quit()


