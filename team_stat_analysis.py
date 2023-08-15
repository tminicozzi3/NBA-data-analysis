# this code pulls data from the stats page on NBA.com
# team stats of interest...
# general -> scoring (others too?), playtype, tracking, shot dashboard, shooting, hustle

import requests
import json
import pandas as pd

def get_url(team_id, year):
    """
    inputs:
        team_id: str, id of team, "0" if want all teams
        year: str, year you want to observe stats for
    output:
        url: the url for the data you want
    """
    url = "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo="+\
    "&Division=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location="+\
    "&MeasureType=Scoring&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N"+\
    "&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N"+\
    "&Season="+year+"&SeasonSegment=&SeasonType=Playoffs&ShotClockRange=&StarterBench="+\
    "&TeamID="+team_id+"&TwoWay=0&VsConference=&VsDivision="
    return url
    return "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Scoring&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2022-23&SeasonSegment=&SeasonType=Playoffs&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision="

def generate_df(url):
    """
    input:
        url: str, url for which we want to generate a dataframe
    output:
        df: dataframe with data from url
    """
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
    
    # create dict
    data = requests.get(url, headers = headers).json()
    # data = json.loads(response.text)

    # create df from dict
    data_headers = data["resultSets"][0]["headers"]
    data_set = data["resultSets"][0]["rowSet"]
    df = pd.DataFrame(data_set, columns = data_headers)

    return df

if __name__ == '__main__':
    # the NBA is hard to analyze because of the talent and style differential between teams
    # and the lack of effort by players during the regular season
    # for our analysis, we will focus on the Milwaukee Bucks playoff performance over a
    # period of years where their core roster has remained largely intact
    # hopefully, this provides some insight on the key drivers of what wins games
    # measure relationship between stat and playoff winning percentage
    milwaukee_id = "1610612749"
    years = ["2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23"]
    url = get_url(milwaukee_id, years[-1])
    d = generate_df(url)
    d = d.drop(columns=[c for c in d.columns if "RANK" in c])
    print(d)
    print(d.columns)
