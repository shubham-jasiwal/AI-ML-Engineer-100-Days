from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_path = "chrome-linux64/chrome"
driver_path = "chromedriver-linux64/chromedriver"

options = Options()
options.binary_location = chrome_path
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)


driver.get("https://www.w3schools.com/howto/howto_css_custom_checkbox.asp")
time.sleep(2)

checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
for box in checkboxes:
    if not box.is_selected():
        box.click()
time.sleep(1)

labels = driver.find_elements(By.CLASS_NAME, "checkcontainer")

for label in labels:
    if "Three" in label.text:
        label.click()
time.sleep(2)
driver.quit()
