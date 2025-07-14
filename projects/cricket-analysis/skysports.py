import requests
import json

# --- Configuration ---
series_id = "1445348"
match_id = "1448349"
inning_number = "4"
from_over = "80"

# --- URL and Headers ---
url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/comments"
params = {
    "lang": "en",
    "seriesId": series_id,
    "matchId": match_id,
    "inningNumber": inning_number,
    "commentType": "ALL",
    "sortDirection": "DESC",
    "fromInningOver": from_over
}

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://www.espncricinfo.com",
    "referer": "https://www.espncricinfo.com/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "x-hsci-auth-token": "exp=1752321741~hmac=8c25a75a0dc46b429c3462f8a33920adfc0bfaa33159828fff0e70ec98764a9b"
}

# --- Request ---
response = requests.get(url, headers=headers, params=params)

# --- Check Response ---
if response.status_code == 200:
    data = response.json()
    comments = data.get("matchCommentary", {}).get("comments", [])
    
    for c in comments:
        over = c.get("over")
        batsman = c.get("batsman", {}).get("name", "N/A")
        bowler = c.get("bowler", {}).get("name", "N/A")
        runs = c.get("runs", {}).get("batsman", 0)
        is_wicket = c.get("isWicket", False)
        text = c.get("comment", "")
        
        print(f"Over {over} | {bowler} to {batsman} | Runs: {runs} | Wicket: {is_wicket}")
        print(f"    ➤ {text}")
        print("-" * 80)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
