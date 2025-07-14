import requests
import json

# Request headers
headers = {
    'accept': '*/*',
    'content-type': 'application/json',
    'fc-device-type': 'desktop',
    'origin': 'https://www.fancode.com',
    'referer': 'https://www.fancode.com/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'source': 'fc-web',
}

parsed = []  # ✅ Move outside loop to accumulate all data

count=85
lastRecordId = 114900000000
while(count > 1):
    print(lastRecordId, "---------------------------")
    
    payload = {
        "operationName": "CricketCommentaryUpdateQuery",
        "operation": "query",
        "variables": {
            "matchId": 112352,
            "commentaryBatch": "OLDER",
            "lastRecordId": f'{lastRecordId}'
        },
        "query": """
        query CricketCommentaryUpdateQuery($matchId: Int!, $lastRecordId: String!, $languageCode: String, $commentaryBatch: String) {
          commentary(
            id: $matchId
            lastRecordId: $lastRecordId
            languageCode: $languageCode
            commentaryBatch: $commentaryBatch
          ) {
            id
            moment {
              ... on Ball {
                value
                ballDetail
                displayNo
                ballNo
              }
              ... on RawContent {
                value
              }
            }
            header
            type
            content {
              ... on EooSummaryContent {
                batsmen { name attributes { runs balls } }
                bowler { name attributes { overs ballsBowled maiden wickets runs } }
                battingTeamInfo { runs overs wickets shortName }
                delivery { runs }
                totalRuns
              }
              ... on RawContent {
                value
              }
            }
          }
        }
        """
    }

    try:
        response = requests.post('https://www.fancode.com/graphql', headers=headers, json=payload)
        data = response.json()

        commentary_data = data.get("data", {}).get("commentary", [])
        
        for item in commentary_data:
            if (item['type'] == 'BALL') and item.get('moment', {}).get('displayNo') and item.get('content', {}).get('value'):
                try:
                    bowler, batsman = item['header'].split(" to ")
                except ValueError:
                    continue  # If "to" split fails, skip this item
                over, ball = item['moment']['displayNo'].split('.')
                parsed.append({
                    "id": item.get("id"),
                    "match_id": "128748",
                    "content": item['content']['value'],
                    "bowler": bowler.strip(),
                    "batsman": batsman.strip(),
                    "over": over,
                    "ball": ball
                })
        lastRecordId = commentary_data[-1].get("id")

    except Exception as e:
        print("❌ Error:", e)
        continue
    count-=1

# ✅ Save all collected data
with open("eng_vs_nz_2024_test-1.json", "w") as f:
    json.dump(parsed, f, indent=2)

print(f"✅ Saved {len(parsed)} commentary entries.")
