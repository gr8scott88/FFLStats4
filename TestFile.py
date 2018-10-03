
import TeamManager as tm
import LeagueManager as lm
import os
import pandas as pd
from bs4 import BeautifulSoup
import SeasonManager as sm




# \venv\Scripts\activate


current_week = 4

sm.load_all_season_data(current_week)



relative_dir = r'data\FFL_Info.csv'
# script_dir = r'C:\Users\gr8sc\PycharmProjects\FFLStats4'
# script_dir = r'C:\Dev\Python\FFLStats4'
script_dir = r'C:\Dev\Python\Projects\FFLStats4'
league_info_file_path = os.path.join(script_dir, relative_dir)
print(league_info_file_path)

week_id = 3

[team_frame, player_frame] = lm.load_league(league_info_file_path, week_id)









team_columns = ['League', 'Team', 'Week', 'Time', 'RealScore', 'ProjScore']
team_frame = pd.DataFrame(columns=team_columns)

player_columns = ['League', 'Team', 'Week', 'Time', 'ActivePos', 'RealScore', 'ProjScore', 'PctPlayed']
player_frame = pd.DataFrame(columns=player_columns)


team_frame

temp_df = pd.DataFrame([1,2,3,4,5,6], columns=team_columns)

arow = [1,2,3,4,5,6]


team_frame.loc[len(team_frame)] = arow