from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

# STEP 1: Yeh paths change kar apne hisaab se
chrome_path = "chrome-linux64/chrome"
driver_path = "chromedriver-linux64/chromedriver"

# STEP 2: Chrome options set karo
options = Options()
options.binary_location = chrome_path
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless")  # headless mode
options.add_argument("--window-size=1280,1024")  # Set size for full screenshot

# options.add_argument("--headless")  # Uncomment for headless mode

# STEP 3: Service object
service = Service(executable_path=driver_path)

# STEP 4: Driver initialize karo
driver = webdriver.Chrome(service=service, options=options)

# STEP 5: Website open karo
# STEP 1: YouTube open karo
# driver.get("https://www.youtube.com")
# time.sleep(2)

# # STEP 2: Accept cookies agar aaya toh skip karna abhi

# # STEP 3: Search box dhoondo (name="search_query" nahi, yeh YouTube hai)
# search_box = driver.find_element(By.NAME, "search_query")

# # STEP 4: Type karo
# search_box.send_keys("lofi music")
# search_box.submit()

# # STEP 5: Wait and print result title
# time.sleep(3)
# print("Search Result Page Title:", driver.title)
# driver.quit()


# STEP 2: Flipkart pe jao
# driver.get("https://www.flipkart.com")
# time.sleep(2)

# # STEP 3: Close login popup (optional)
# try:
#     close_btn = driver.find_element(By.XPATH, "//button[contains(text(),'✕')]")
#     close_btn.click()
#     print("Login popup closed ✅")
# except:
#     print("No login popup found ❌")

# # STEP 4: Search "shoes"
# search_box = driver.find_element(By.NAME, "q")
# search_box.send_keys("shoes")
# search_box.submit()
# time.sleep(3)

# # STEP 5: Product titles and prices
# # STEP 5: Get titles using correct classes for shoes
# brands = driver.find_elements(By.CLASS_NAME, "syl9yP")  # brand name
# titles = driver.find_elements(By.CLASS_NAME, "WKTcLC")    # product description
# prices = driver.find_elements(By.CLASS_NAME, "Nx9bqj")  # price


# print("\n🛒 Top 10 Shoes:")
# for i in range(min(10, len(titles), len(prices))):
#     brand = titles[i].text
#     desc = descs[i].text if i < len(descs) else ""
#     price = prices[i].text
#     print(f"{i+1}. {brand} - {desc} - {price}")

# data = []
# for i in range(min(10, len(brands), len(prices))):
#     data.append({
#         "Brand": brands[i].text,
#         "Title": titles[i].text if i < len(titles) else "",
#         "Price": prices[i].text
#     })

# # Export to CSV
# df = pd.DataFrame(data)
# df.to_csv("flipkart_shoes.csv", index=False, encoding='utf-8-sig')

# print("✅ Data exported to flipkart_shoes.csv")

# driver.quit()


# STEP 1: Open Instagram
# driver.get("https://www.instagram.com/accounts/login/")
# time.sleep(5)  # wait to load fully

# # STEP 2: Screenshot
# screenshot_file = "instagram_login.png"
# driver.save_screenshot(screenshot_file)
# print(f"✅ Screenshot saved as {screenshot_file}")

# driver.quit()


# STEP 2: Open Google Form
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdeBv.../viewform"
driver.get(form_url)
time.sleep(4)

# STEP 3: Locate Fields and Fill
fields = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')

# Fill Name
fields[0].send_keys("Shubham Kumar")
# Fill Email
fields[1].send_keys("shubham@example.com")

# STEP 4: Submit
submit_btn = driver.find_element(By.XPATH, '//span[text()="Submit"]')
submit_btn.click()

# STEP 5: Wait for confirmation
time.sleep(3)
print("✅ Form submitted successfully!")

driver.quit()