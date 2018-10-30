
import Team as tm
import League as lm
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests


url = r'https://football.fantasysports.yahoo.com/f1/910981'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

t = soup.find_all('ul', class_='List-rich')
p = t[0].find_all('a', class_='F-link')


import League
league_id = 910981
league = League.League(league_id)

#league.load_single_week_data(1)

# league.load_data_point(1, 0)
league.load_data_point(2, 0)

import Team
team_id = 1
team = Team.Team(league_id, team_id)
team.load_soup_for_week(1, 0)
team_data = team.parse_team_info()

player_data = team.parse_all_player_info()