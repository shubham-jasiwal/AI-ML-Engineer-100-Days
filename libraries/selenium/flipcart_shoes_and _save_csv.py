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
options.add_argument("--headless")  
options.add_argument("--window-size=1280,1024") 



service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service, options=options)



driver.get("https://www.flipkart.com")
time.sleep(2)

try:
    close_btn = driver.find_element(By.XPATH, "//button[contains(text(),'✕')]")
    close_btn.click()
    print("Login popup closed ✅")
except:
    print("No login popup found ❌")


search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("shoes")
search_box.submit()
time.sleep(3)


brands = driver.find_elements(By.CLASS_NAME, "syl9yP")  # brand name
titles = driver.find_elements(By.CLASS_NAME, "WKTcLC")    # product description
prices = driver.find_elements(By.CLASS_NAME, "Nx9bqj")  # price


data = []
for i in range(min(10, len(brands), len(prices))):
    data.append({
        "Brand": brands[i].text,
        "Title": titles[i].text if i < len(titles) else "",
        "Price": prices[i].text
    })


df = pd.DataFrame(data)
df.to_csv("flipkart_shoes.csv", index=False, encoding='utf-8-sig')

print("✅ Data exported to flipkart_shoes.csv")

driver.quit()