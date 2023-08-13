# this code pulls data from the stats page on NBA.com
# team stats of interest...
# general -> scoring (others too?), playtype, tracking, shot dashboard, shooting, hustle

import requests
import json
import pandas as pd

def generate_df(url, headers):
    """
    input:
        url: str, url for which we want to generate a dataframe
    output:
        df: dataframe with data from url
    """
    # create dict
    data = requests.get(url, headers = headers).json()
    # data = json.loads(response.text)

    # create df from dict
    data_headers = data["resultSets"][0]["headers"]
    data_set = data["resultSets"][0]["rowSet"]
    df = pd.DataFrame(data_set, columns = data_headers)

    return df

if __name__ == '__main__':
    url = "https://stats.nba.com/stats/leaguedashteamptshot?CloseDefDistRange=&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=&GameScope=&GameSegment=&GeneralRange=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2022-23&SeasonSegment=&SeasonType=Regular%20Season&ShotClockRange=7-4%20Late&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange=&VsConference=&VsDivision=&Weight="
    headers = {"Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Host": "stats.nba.com",
    "Origin": "https://www.nba.com",
    "Referer": "https://www.nba.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"}
    d = generate_df(url, headers)
    print(d)
