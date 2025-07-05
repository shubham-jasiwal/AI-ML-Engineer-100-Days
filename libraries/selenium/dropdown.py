from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

chrome_path = "chrome-linux64/chrome"
driver_path = "chromedriver-linux64/chromedriver"

options = Options()
options.binary_location = chrome_path
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)


driver.get("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select")
time.sleep(2)


driver.switch_to.frame("iframeResult")

dropdown = Select(driver.find_element(By.ID, "cars"))

dropdown.select_by_visible_text("Audi")
time.sleep(1)

selected = dropdown.first_selected_option
print(f"Selected: {selected.text}")
selected.submit()
time.sleep(2)

----------------------------------------------Alternate---------------------------------------

dropdown = Select(driver.find_element(By.TAG_NAME, "select"))

dropdown.select_by_visible_text("Saab")

selected = dropdown.first_selected_option
print(f"Selected option: {selected.text}")


driver.quit()
