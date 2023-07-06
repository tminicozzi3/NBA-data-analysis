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

def get_df(player_id, year, regular_or_post_season, context, team_id = 0):
    """
    inputs:
        team_id: int, default is 0 (looks at all shots player takes no matter team they are on)
        player_id: int, id number of player in data
        year: str, of the form yyyy-yy
        regular_or_post_season: str, either "Regular Season", "Playoffs", "Pre Season"
            or "All Star"
        context: str, see shotchartdetail github documentation
    output:
        json file containing requested data
    """
    # get the json -> python dictionary using shotchartdetail
    data = shotchartdetail.ShotChartDetail(
        team_id=team_id,
        player_id=player_id,
        season_nullable=year,
        season_type_all_star=regular_or_post_season,
        context_measure_simple = context
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
        d: dataframe, which will be generated from the function get_df
        color: color of the text
    output:
        shot chart, which is a matplotlib plot
    """
    # dimensions of court found using NBA rule book
    # https://official.nba.com/rule-no-1-court-dimensions-equipment/
    # our hoop will be at (0,0)
    plt.xlim(-250,250)
    plt.ylim(470 - 54.2, - 54.2)
    # use image as court instead of drawing lines
    court = plt.imread("warriors-court.png")
    plt.imshow(court, extent = [-250, 250, 470 - 54.2, - 54.2])
    # look at percentages by zone
    zones = []
    # each zone of interest is a combo of SHOT_ZONE_AREA:
    # {'Center(C)', 'Right Side Center(RC)', 'Left Side Center(LC)',
    # 'Right Side(R)', 'Back Court(BC)', 'Left Side(L)'}
    # and SHOT_ZONE_BASIC:
    # {'Backcourt', 'Restricted Area', 'Above the Break 3', 'Right Corner 3',
    # 'Left Corner 3', 'In The Paint (Non-RA)', 'Mid-Range'}
    for pos in set(d["SHOT_ZONE_AREA"]):
        for dis in set(d["SHOT_ZONE_BASIC"]):
            if dis != "In The Paint (Non-RA)":
                zones.append((pos, dis))
    # only want one zone for shots in the paint outside of RA
    zones.append(("", "In The Paint (Non-RA)"))
    # loop through each zone to find makes and misses in each zone
    for pos, dis in zones:
        if pos:
            d_make = d[(d["SHOT_MADE_FLAG"] == 1) & (d["SHOT_ZONE_AREA"] == pos)
                & (d["SHOT_ZONE_BASIC"] == dis)]
            d_miss = d[(d["SHOT_MADE_FLAG"] == 0) & (d["SHOT_ZONE_AREA"] == pos)
                & (d["SHOT_ZONE_BASIC"] == dis)]
        else:
            d_make = d[(d["SHOT_MADE_FLAG"] == 1) & (d["SHOT_ZONE_BASIC"] == dis)]
            d_miss = d[(d["SHOT_MADE_FLAG"] == 0) & (d["SHOT_ZONE_BASIC"] == dis)]
        if len(d_make)+len(d_miss) != 0:
            # scatter shots on chart
            plt.scatter(d_make["LOC_X"], d_make["LOC_Y"], alpha = .2, color = "green")
            plt.scatter(d_miss["LOC_X"], d_miss["LOC_Y"], alpha = .1, color = "red")
            # add percentage in each zone of interest
            # the text shows up where the avaerage shot in that zone was taken from
            plt.text(pd.concat([d_make, d_miss])["LOC_X"].mean(),
                pd.concat([d_make, d_miss])["LOC_Y"].mean(),
                    str(round(100*len(d_make)/(len(d_make)+len(d_miss)),1)) + "%",
                        color = color, fontsize = 12.0, fontweight = "bold")
    
    plt.show()


jp_id = get_player_id("kyrie irving")

d = get_df(jp_id, "2022-23", "Regular Season", "FGA")

print(d)

print(d["LOC_Y"])
print(d["LOC_X"], set(d["SHOT_ZONE_AREA"]))
print(d["SHOT_MADE_FLAG"])
print(set(d["SHOT_ZONE_BASIC"]))
print(set(d["SHOT_ZONE_BASIC"]).difference(set("In The Paint (Non-RA)")))
print(players.find_players_by_full_name("jordan poole"))

draw_court(d)

# ideas...
# make zones uniform
# use player index to find height
# percentage by location, defender (height??), home vs away (lots of players), assisted vs not
# open vs contested
# compared to league avgs!!! - remember this is in data
# analyze teams in this way
# ... have a ton of functions that perform different analysis
