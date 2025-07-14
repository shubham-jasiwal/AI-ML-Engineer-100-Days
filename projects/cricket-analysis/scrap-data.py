from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Optional headless setup
options = Options()
# options.add_argument('--headless')  # Uncomment for headless

driver = webdriver.Chrome(options=options)
driver.get("https://www.cricbuzz.com/cricket-full-commentary/105762/eng-vs-ind-1st-test-india-tour-of-england-2025")
time.sleep(5)

# STEP 1: Click on "IND 1st Inns" or any other innings tab
try:
    innings_tab = driver.find_element(By.XPATH, "//a[contains(text(),'IND 1st Inns')]")
    innings_tab.click()
    print("Clicked on innings tab.")
    time.sleep(3)
except Exception as e:
    print("Could not click innings tab:", e)

# STEP 2: Scrape ball-by-ball data
deliveries = []

blocks = driver.find_elements(By.CSS_SELECTOR, "div.cb-col.cb-col-100.ng-scope")
for block in blocks:
    try:
        over = block.find_element(By.CLASS_NAME, "cb-ovr-num").text.strip()
        text = block.find_element(By.CLASS_NAME, "cb-com-ln").text.strip()

        bowler, batter = None, None
        parts = text.split(",")[0].split(" to ")
        if len(parts) == 2:
            bowler = parts[0].strip()
            batter = parts[1].strip()

        # Basic ball type and action inference
        ball_type = "unknown"
        batsman_action = "unknown"
        if "full" in text:
            ball_type = "full"
        elif "short" in text:
            ball_type = "short"
        elif "length" in text:
            ball_type = "length"

        if "pull" in text:
            batsman_action = "pull shot"
        elif "block" in text:
            batsman_action = "defensive block"
        elif "cut" in text:
            batsman_action = "cut shot"

        deliveries.append({
            "over": over,
            "text": text,
            "bowler": bowler,
            "batter": batter,
            "ball_type": ball_type,
            "batsman_action": batsman_action
        })

    except Exception:
        continue

driver.quit()

# STEP 3: Save as JSON
import json
with open("match_data.json", "w") as f:
    json.dump(deliveries, f, indent=2)

print("Saved", len(deliveries), "deliveries to match_data.json")
