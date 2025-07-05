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



driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)  # wait to load fully


screenshot_file = "instagram_login.png"
driver.save_screenshot(screenshot_file)
print(f"✅ Screenshot saved as {screenshot_file}")

driver.quit()


