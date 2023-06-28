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
    input player name: str, not case sensitive
    output: player_id if valid player and only one player by that name
            -1 if not a valid player or there are more than one player with the name
    """
    list_player = players.find_players_by_full_name(player_name)
    if len(list_player) == 1:
        return list_player[0]["id"]
    else:
        return -1

jp_id = get_player_id("jordan poole")
print(jp_id)

jp_data = shotchartdetail.ShotChartDetail(
    team_id=0,
    player_id=jp_id,
    season_nullable='2022-23',
    season_type_all_star='Regular Season'
)

print(json.loads(jp_data.get_json()))
