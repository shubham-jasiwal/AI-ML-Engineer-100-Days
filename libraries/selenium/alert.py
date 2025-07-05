from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_path = "/home/yourname/Downloads/chrome-linux64/chrome"
driver_path = "/home/yourname/Downloads/chromedriver-linux64/chromedriver"

options = Options()
options.binary_location = chrome_path
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://demo.automationtesting.in/Alerts.html")
driver.maximize_window()
time.sleep(2)

driver.find_element(By.CLASS_NAME, "btn-danger").click()
time.sleep(1)
alert = driver.switch_to.alert
print("Alert text:", alert.text)
alert.accept()  # Press OK

driver.find_element(By.LINK_TEXT, "Alert with OK & Cancel").click()
driver.find_element(By.CLASS_NAME, "btn-primary").click()
time.sleep(1)
alert = driver.switch_to.alert
print("Confirm text:", alert.text)
alert.dismiss()  # Press Cancel

driver.find_element(By.LINK_TEXT, "Alert with Textbox").click()
driver.find_element(By.CLASS_NAME, "btn-info").click()
time.sleep(1)
alert = driver.switch_to.alert
print("Prompt text:", alert.text)
alert.send_keys("Shubham")
alert.accept()

time.sleep(2)
driver.quit()
