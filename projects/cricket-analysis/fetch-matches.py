import requests
import json
import csv

team_shortName = ["IND", "AUS", "ENG", "PAK", "NZ", "SA", "BAN", "SL", "AFG", "WI", "IRE", "ZIM", "NED", "SCO", "NEP", "OMA", "UAE", "USA", "PNG", "NAM", "CAN", "HK", "BER", "UGA", "KEN"]

team_full_names = {
    "IND": "India", "AUS": "Australia", "ENG": "England", "PAK": "Pakistan", "NZ": "New Zealand",
    "SA": "South Africa", "BAN": "Bangladesh", "SL": "Sri Lanka", "AFG": "Afghanistan", "WI": "West Indies",
    "IRE": "Ireland", "ZIM": "Zimbabwe", "NED": "Netherlands", "SCO": "Scotland", "NEP": "Nepal", "OMA": "Oman",
    "UAE": "United Arab Emirates", "USA": "United States of America", "PNG": "Papua New Guinea",
    "NAM": "Namibia", "CAN": "Canada", "HK": "Hong Kong", "BER": "Bermuda", "UGA": "Uganda", "KEN": "Kenya"
}

url = 'https://www.fancode.com/graphql'

headers = {
    'accept': '*/*',
    'content-type': 'application/json',
    'origin': 'https://www.fancode.com',
    'referer': 'https://www.fancode.com/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)',
    'fc-device-type': 'desktop',
    'source': 'fc-web'
}

query_string = """
fragment authorizationInfo on AuthorizationInfo {
  contentName
  priceInfo {
    price { value currency { symbol } }
    discountedPrice { value currency { symbol } }
  }
  bgImage { src }
}

fragment squadsFragment on Squad {
  flag { src }
  name
  squadNo
  shortName
  isWinner
  cricketScore {
    runs
    overs
    balls
    status
    wickets
  }
}

fragment matchDetailsScoreCard on ScoreCard {
  cricketScore {
    description
    newDescription
    innings {
      number
      battingTeamShortName
      runs
      wickets
      overs
      balls
    }
    matchInfo {
      description
      matchDay
      session
    }
    cricketCurrentOverDetails {
      batsmen {
        shortName
        attributes {
          runs
          balls
        }
      }
    }
  }
}

query MatchDetailsScoreResponse($id: Int!, $hasAdTechSDK: Boolean!, $videoProtocols: [VideoProtocols!], $drmInfra: DRMInfra, $ssaiInfra: SSAIInfra, $currentVideoSource: VideoSourceInput, $sessionInfraAvailable: Boolean!, $wmInfra: WMInfra) {
  match: matchWithScores(
    id: $id
    hasAdTechSDK: $hasAdTechSDK
    videoProtocols: $videoProtocols
    drmInfra: $drmInfra
    ssaiInfra: $ssaiInfra
    currentVideoSource: $currentVideoSource
    sessionInfraAvailable: $sessionInfraAvailable
    wmInfra: $wmInfra
  ) {
    id
    mediaId
    format
    streamingStatus
    isScorecardAvailable
    isPremium
    isUserEntitled
    isAdFundedEntitled
    status
    matchStatusDescription
    squads { ...squadsFragment }
    streamAuthorization {
      authorizationType
      authorizationInfo { ...authorizationInfo }
    }
    dayStartTime
    scorecard { ...matchDetailsScoreCard }
    showUpgradeCta
    streamStatusPolling
    streamStatusPollingIntervalInSec
  }
}
"""
match_data = []

for matchId in range(110000, 120000):
    payload = {
        "operationName": "MatchDetailsScoreResponse",
        "variables": {
            "id": matchId,
            "hasAdTechSDK": True,
            "drmInfra": {"drmType": "WIDEVINE", "securityLevel": "LEVEL_3"},
            "ssaiInfra": {"providers": ["YOSPACE"]},
            "currentVideoSource": {"drmProvider": "NONE", "ssaiProvider": "NONE", "isCasting": False},
            "wmInfra": {"active": True, "visible": False},
            "videoProtocols": ["HLS", "DASH"],
            "sessionInfraAvailable": True
        },
        "query": query_string
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            data = response.json()
            match = data['data']['match']
            innings = match['scorecard']['cricketScore']['innings']
            print(team_full_names[innings[0]['battingTeamShortName']], match['squads'][0]['name'])
            if(team_full_names[innings[0]['battingTeamShortName']] == match['squads'][0]['name']):
                
                print("===================================================================")
                print(f"Match ID: {matchId}")
                print("Format:", match['format'])
                print("Teams:", match['squads'][0]['shortName'], "vs", match['squads'][1]['shortName'])
                print("Description:", match['scorecard']['cricketScore']['description'])
                print("Innings 1:", innings[0]['battingTeamShortName'])
                print("Innings 2:", innings[1]['battingTeamShortName'])
                print("Match Info:", match['scorecard']['cricketScore']['matchInfo']['description'])
                print("===================================================================")
                row = {
                    "match_id": matchId,
                    "format": match['format'],
                    "team_1": match['squads'][0]['shortName'],
                    "team_2": match['squads'][1]['shortName'],
                    "description": match['scorecard']['cricketScore']['description'],
                    "team_1_runs": innings[0]['runs'],
                    "team_1_wickets": innings[0]['wickets'],
                    "team_1_overs": innings[0]['overs'],
                    "team_2_runs": innings[1]['runs'],
                    "team_2_wickets": innings[1]['wickets'],
                    "team_2_overs": innings[1]['overs'],
                    "match_info": match['scorecard']['cricketScore']['matchInfo']['description']
                }
                match_data.append(row)
        except Exception as e:
            print("❌ Error parsing response:", e)
    else:
        print(f"❌ Request failed with status code {response.status_code} for matchId {matchId}")

csv_file = "match_data-2.csv"
fieldnames = [
    "match_id", "format", "team_1", "team_2", "description",
    "team_1_runs", "team_1_wickets", "team_1_overs",
    "team_2_runs", "team_2_wickets", "team_2_overs", "match_info"
]

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(match_data)

print(f"\n✅ Saved {len(match_data)} matches to {csv_file}")
