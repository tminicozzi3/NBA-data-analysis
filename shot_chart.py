# this code uses the nba_api package:
# https://pypi.org/project/nba-api/
# specifically, it uses shotchartdetail:
# https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/shotchartdetail.md

# imports
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def get_player_id(player_name):
    """
    inputs:
        player name: str, not case sensitive
    output:
        player_id if valid player and only one player by that name
        -1 if not a valid player or there are more than one player with the name
    """
    list_player = players.find_players_by_full_name(player_name)
    if len(list_player) == 1:
        return list_player[0]["id"]
    else:
        return -1

def get_df(player_id, year, regular_or_post_season, team_id = 0):
    """
    inputs:
        team_id: int, default is 0 (looks at all shots player takes no matter team they are on)
        player_id: int, id number of player in data
        year: str, of the form yyyy-yy
        regular_or_post_season: str, either "Regular Season", "Playoffs", "Pre Season"
            or "All Star"
    output:
        json file containing requested data
    """
    # get the json -> python dictionary using shotchartdetail
    data = shotchartdetail.ShotChartDetail(
        team_id=team_id,
        player_id=player_id,
        season_nullable=year,
        season_type_all_star=regular_or_post_season
    )
    data_json = json.loads(data.get_json())

    # get the dataframe from the dictionary
    rows = data_json["resultSets"][0]["rowSet"]
    df = pd.DataFrame(rows)
    df.columns = data_json["resultSets"][0]["headers"]
    return df

def draw_court(d, color = "black"):
    """
    inputs:
        x
    output:
        shot chart, matplotlib plot
    """
    # dimensions of court found using NBA rule book
    # https://official.nba.com/rule-no-1-court-dimensions-equipment/
    # our hoop will be at (0,0)
    plt.xlim(-250,250)
    plt.ylim(470 - 54.2, - 54.2)
    # use image as court instead of drawing lines
    court = plt.imread("warriors-court.png")
    plt.imshow(court, extent = [-250, 250, 470 - 54.2, - 54.2])
    plt.scatter(d["LOC_X"], d["LOC_Y"], alpha = .3)
    plt.show()


jp_id = get_player_id("jordan poole")

d = get_df(jp_id, "2022-23", "Regular Season")

print(d)

print(d["LOC_Y"])
print(d["LOC_X"], d["SHOT_ZONE_AREA"])

draw_court(d)
