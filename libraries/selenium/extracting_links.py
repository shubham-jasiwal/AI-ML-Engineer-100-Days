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


driver.get("https://www.w3schools.com/html/html_links.asp")
time.sleep(2)

links = driver.find_elements(By.TAG_NAME, "a")
print(f"Total Links Found: {len(links)}\n")


for i, link in enumerate(links[:10]):
    href = link.get_attribute("href")
    if href and href.startswith("http"):  
        print(f"{i+1}. {link.text.strip()} --> {link.get_attribute('href')}")

driver.quit()
