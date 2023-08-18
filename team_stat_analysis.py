# this code pulls data from the stats page on NBA.com
# 
# team stats of interest...
# general -> scoring (others too?), playtype, tracking, shot dashboard, shooting, hustle

import requests
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def get_url_pct_shots(team_id, year):
    """
    inputs:
        team_id: str, id of team, "0" if want all teams
        year: str, year you want to observe stats for
    output:
        url: the url for the data you want
    """
    # this url is for the stats page that shows percentages of total scoring that come
    # from various shot types
    url = "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo="+\
    "&Division=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location="+\
    "&MeasureType=Scoring&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N"+\
    "&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N"+\
    "&Season="+year+"&SeasonSegment=&SeasonType=Playoffs&ShotClockRange=&StarterBench="+\
    "&TeamID="+team_id+"&TwoWay=0&VsConference=&VsDivision="
    return url

def get_url_four_factors(team_id, year):
    """
    inputs:
        team_id: str, id of team, "0" if want all teams
        year: str, year you want to observe stats for
    output:
        url: the url for the data you want
    """
    # this url is for the four factors stats page
    url = "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo="+\
    "&Division=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location="+\
    "&MeasureType=Four%20Factors&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N"+\
    "&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N"+\
    "&Season="+year+"&SeasonSegment=&SeasonType=Playoffs&ShotClockRange=&StarterBench="+\
    "&TeamID="+team_id+"&TwoWay=0&VsConference=&VsDivision="
    return url

def get_url_advanced(team_id, year):
    """
    inputs:
        team_id: str, id of team, "0" if want all teams
        year: str, year you want to observe stats for
    output:
        url: the url for the data you want
    """
    # this url is for the advanced stats page
    url = "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo="+\
    "&Division=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location="+\
    "&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N"+\
    "&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N"+\
    "&Season="+year+"&SeasonSegment=&SeasonType=Playoffs&ShotClockRange=&StarterBench="+\
    "&TeamID="+team_id+"&TwoWay=0&VsConference=&VsDivision="
    return url

def generate_df(url, year):
    """
    input:
        url: str, url for which we want to generate a dataframe
        year: str, year YYYY-YY
    output:
        df: dataframe with data from url
    """
    # need to include headers to be able to access data
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
    # create df from dict
    data_headers = data["resultSets"][0]["headers"]
    data_set = data["resultSets"][0]["rowSet"]
    df = pd.DataFrame(data_set, columns = data_headers)
    # add a year column to data
    df["YEAR"] = year

    return df

def generate_all_data_df(urls, years):
    """
    input:
        urls: list of str, url for which we want to generate a dataframe
        years: list of str of form YYYY-YY
    output:
        df: dataframe with data from url over all years
    """
    # loop through the data corresponding to different years
    df = generate_df(urls[0], years[0])
    for url, year in zip(urls[1:],years[1:]):
        # create the df for the data
        new_df = generate_df(url, year)
        # add that df to the all years df
        df = pd.concat([df, new_df], axis = 0)
    df = df.drop(columns=[c for c in df.columns if "RANK" in c])
    return df

def calc_r2(df):
    """
    input:
        df: dataframe with data of interest
    output:
        lst_r2: list of tuple...(stat, r2 value of stat wrt win pct)
    """
    # stats of interest
    metrics = [c for c in df.columns
        if (c not in ["TEAM_ID", "TEAM_NAME", "GP", "W", "L", "W_PCT", "MIN", "YEAR"])]
    dict_r2 = {}
    # loop through stats
    for metric in metrics:
        # create a linear regression model with appropriate data
        model = LinearRegression()
        X, y = np.array(df[metric]).reshape(-1, 1), np.array(df["W_PCT"])
        model.fit(X, y)
        # find r2 value and add to list
        dict_r2[metric] = round(model.score(X, y), 3)
    return dict_r2

if __name__ == '__main__':
    # the NBA is hard to analyze because of the talent and style differential between teams
    # and the lack of effort by players during the regular season
    # for our analysis, we will focus on the Milwaukee Bucks playoff performance over a
    # period of years where their core roster has remained largely intact
    # hopefully, this provides some insight on the key drivers of what wins playoff games
    # (for the Milwaukee Bucks)
    # use Linear Regression to measure relationship between stat and playoff winning percentage
    milwaukee_id = "1610612749"
    years = ["2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23"]
    urls1 = [get_url_pct_shots(milwaukee_id, year) for year in years]
    d1 = generate_all_data_df(urls1, years)
    urls2 = [get_url_advanced(milwaukee_id, year) for year in years]
    d2 = generate_all_data_df(urls2, years)
    urls3 = [get_url_four_factors(milwaukee_id, year) for year in years]
    d3 = generate_all_data_df(urls3, years)

    for d in [d1,d2,d3]:
        print(sorted(calc_r2(d).items(), key = lambda x: x[1], reverse = True))