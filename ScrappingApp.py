import streamlit as st
import requests
import json
import pandas as pd 
import numpy as np
import datetime

url_get_matches = "https://www.my11circle.com/api/lobbyApi/v1/getMatches"
url_get_players = "https://www.my11circle.com/api/lobbyApi/matches/v1/getMatchSquad"

get_match_body = json.dumps({"sportsType":1,"isNonCashAppVersion":"false"})

headers = {
"Host": "www.my11circle.com",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
"Accept": "application/json, text/plain, */*",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding": "gzip, deflate, br",
"Referer": "https://www.my11circle.com/mecspa/lobby/",
"Origin": "https://www.my11circle.com",
"Connection": "keep-alive",
"Cookie": "device.info.cookie={'bv':'102.0','bn':'Firefox','osv':'10','osn':'Windows','tbl':'false','vnd':'false','mdl':'false'}; _scid=09487f3b-5f18-45d7-ae57-9209e252e102; _sctr=1|1657650600000; _fbp=fb.1.1657715741422.5891218; _ga=GA1.2.291971472.1657715742; _gid=GA1.2.1774856958.1657715742; cto_bundle=IQsNJV9UdDJmZ3dPdnozdmVmMktUSVNhSFZObWtZNW54c2Y0eDVaYzFnaSUyRmlZT2QwYTladFlsQXlKN2ZjQUxINUp3aXY2Zk5uWkRTa2ZtYWRyaks4NXRQMUR3Vnp6clAxaks4cEk0UHlQNm0ydXoxNlE1OHEwWGdQcEhsWGxZeGRUNGR3VGVrMDloelpqSTAzJTJCNyUyQmpvMXpSN3clM0QlM0Q; SSIDuser=SSIDd6f76e0f-15c0-4a32-ad6b-f0fb043e94ce%3A101967836; sameSiteNoneSupported=true; NA_VISITOR=c6cb8d13-881f-45b7-bf7e-35649934f8ec; SSID=SSIDd6f76e0f-15c0-4a32-ad6b-f0fb043e94ce; ga24x7_pixeltracker=",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "no-cors",
"Sec-Fetch-Site": "same-origin",
"Content-Type": "application/json;charset=utf-8",
"Pragma": "no-cache",
"Cache-Control": "no-cache"
}

st.set_page_config(
     page_title="MatchDataScraper",
     page_icon="⛏",
     layout="wide",
 )

st.title("My 11 Circle Match Data Scraper")

cookie = st.text_input("Enter the Cookie...")

headers['Cookie'] = cookie

if st.button("Process"):
    data = requests.post(url_get_matches, get_match_body, headers=headers)
    data = data.json()
    matchids = {}
    for match in data['matches']['1']:
        matchids[match['matchId']] = match['team1']['dName']+ ' vs ' + match['team2']['dName']
    
    match = []
    name = []
    teamName = []
    roleName = []
    credits = []

    for id in matchids:
        get_match_squard_body = {"matchId":0}
        get_match_squard_body['matchId'] = id
        get_match_squard_body = json.dumps(get_match_squard_body)
        try:
            match_data =  requests.post(url_get_players, get_match_squard_body, headers=headers).json()
            for player in match_data['players']:
                match.append(matchids[id])
                name.append(player['name'])
                teamName.append(player['teamName'])
                roleName.append(player['roleName'])
                credits.append(player['credits'])
        except:
            match.append(matchids[id])
            name.append('')
            teamName.append('')
            roleName.append('')
            credits.append('')

    df = pd.DataFrame()
    df['Match'] = match
    df['Player Name'] = name
    df['Team Name'] = teamName
    df['Player Role'] = roleName
    df['Credits'] = credits

    excel = df.to_csv(index=False).encode('utf-8')
    st.download_button(
    "Download",
    excel,
    "%s_My11CircleData.csv"%datetime.date.today(),
    "text/csv",
    key='download-csv'
    )