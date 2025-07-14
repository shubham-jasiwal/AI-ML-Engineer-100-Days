import csv
import json
import requests
import os

# Headers for the GraphQL request
headers = {
    'accept': '*/*',
    'content-type': 'application/json',
    'fc-device-type': 'desktop',
    'origin': 'https://www.fancode.com',
    'referer': 'https://www.fancode.com/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'source': 'fc-web',
}

# Path to the CSV file with match data
csv_path = "match_data.csv"

# Output directory
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Read matches from CSV
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        match_id = int(row['match_id'])
        format_ = row['format']
        team_1 = row['team_1']
        team_2 = row['team_2']
        match_info = row['match_info'].replace(" ", "_").replace("/", "-")  # sanitize
        filename = f"{match_id}-{team_1}-{team_2}-{format_}-{match_info}.json"
        filepath = os.path.join(output_dir, filename)

        print(f"🔍 Processing match: {match_id} ({team_1} vs {team_2})")

        # GraphQL pagination loop
        parsed = []
        lastRecordId = 114900000000
        count = 100
        while count > 1:
            payload = {
                "operationName": "CricketCommentaryUpdateQuery",
                "operation": "query",
                "variables": {
                    "matchId": match_id,
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

                if not commentary_data:
                    break  # No more data to fetch

                for item in commentary_data:
                    if (item['type'] == 'BALL') and item.get('moment', {}).get('displayNo') and item.get('content', {}).get('value'):
                        try:
                            bowler, batsman = item['header'].split(" to ")
                        except ValueError:
                            continue
                        over, ball = item['moment']['displayNo'].split('.')
                        parsed.append({
                            "id": item.get("id"),
                            "match_id": match_id,
                            "content": item['content']['value'],
                            "bowler": bowler.strip(),
                            "batsman": batsman.strip(),
                            "over": over,
                            "ball": ball,
                            "value": item['moment']['value'],
                            "ballDetail": item['moment']['ballDetail']
                        })

                lastRecordId = commentary_data[-1].get("id")

            except Exception as e:
                print(f"❌ Error fetching commentary for match {match_id}: {e}")
                break
            count -= 1

        # Save to file
        if parsed:
            with open(filepath, "w", encoding='utf-8') as f:
                json.dump(parsed, f, indent=2)
            print(f"✅ Saved {len(parsed)} entries to {filename}")
        else:
            print(f"⚠️ No commentary data found for match {match_id}")
