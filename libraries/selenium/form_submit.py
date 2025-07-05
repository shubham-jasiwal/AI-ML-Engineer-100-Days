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


driver.get("https://www.w3schools.com/html/html_forms.asp")
time.sleep(2)


name_input = driver.find_element(By.ID, "fname")
name_input.clear()
name_input.send_keys("Shubham")

submit_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Submit")]')
submit_btn.click()


time.sleep(3)
print("✅ Form submitted.")
driver.quit()
