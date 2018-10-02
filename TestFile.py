
import TeamManager as tm
import LeagueManager as lm
import os
import pandas as pd

# \venv\Scripts\activate


# url = r"week3test.html"

ex_url = 'https://football.fantasysports.yahoo.com/f1/910981/4/team?&week=3'
ex_saved_html = r'week3test.html'

# get_all_info(team_info)


league = '910981'
team = '4'
week = '3'
# loaded_soup = get_soup_single(league, team, week)

loaded_soup = tm.load_soup_single(ex_saved_html)
all_week_info = tm.get_player_info(loaded_soup)


for player in all_week_info:
    print(player)


relative_dir = r'/data/FFL_Info.csv'
script_dir = r'C:/Users/gr8sc\PycharmProjects/FFLStats4'
file_dir = os.path.join(script_dir, relative_dir)
lm.load_league(file_dir)
