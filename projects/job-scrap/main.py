from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_path = "chrome-linux64/chrome"
driver_path = "chromedriver-linux64/chromedriver"


options = Options()
options.binary_location = chrome_path
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1280,1024") 



service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)


driver.get("https://www.naukri.com/mnjuser/homepage")
time.sleep(2)

email_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Email ID']")
email_input.send_keys("your_email_id(naukari)")

time.sleep(1)

password_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Password']")
password_input.send_keys("password")

login_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Login")]')
login_btn.click()
time.sleep(2)

keywords = ['django','fastapi','aws','pandas','numpy','selenium','machine learning']
for key in keywords:
    jobs = []
    for page in range(1, 6):  # Pages 1 to 5
        if page == 1:
            url = f"https://www.naukri.com/python-plus-{key}-jobs"
        else:
            url = f"https://www.naukri.com/python-plus-{key}-jobs-{page}"

        driver.get(url)
        time.sleep(5)  # Let page load

        job_cards = driver.find_elements(By.CLASS_NAME, "cust-job-tuple")
        print(f"✅ Page {page} — Found {len(job_cards)} jobs")

        for job in job_cards[:20]:
            try:
                print("------------------------------------------1-------------------------------")
                title = job.find_element(By.CSS_SELECTOR, "a.title").text
                link = job.find_element(By.CSS_SELECTOR, "a.title").get_attribute("href")
                company = job.find_element(By.CSS_SELECTOR, "a.comp-name").text
                location = job.find_element(By.CSS_SELECTOR, "span.locWdth").text
                experience = job.find_element(By.CSS_SELECTOR, "span.expwdth").text
                description = job.find_element(By.CSS_SELECTOR, "span.job-desc").text
                posted = job.find_element(By.CSS_SELECTOR, "span.job-post-day").text
                
                tags = [tag.text for tag in job.find_elements(By.CSS_SELECTOR, "ul.tags-gt li")]
                print(title,company,location,experience)

                jobs.append({
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Experience": experience,
                    "Description": description,
                    "Apply Link": link,
                    "Tags": ", ".join(tags),
                    "Posted": posted
                })
            except:
                continue

     # Save to CSV
        df = pd.DataFrame(jobs)
        df.to_csv(f"/output/naukri_{key}_jobs.csv", index=False, encoding="utf-8-sig")
        print(f"✅ Scraped total {len(jobs)} jobs across 5 pages.")


driver.quit()