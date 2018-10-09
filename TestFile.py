
import TeamManager as tm
import LeagueManager as lm
import os
import pandas as pd
from bs4 import BeautifulSoup
import SeasonManager as sm








# \venv\Scripts\activate


current_week = 4


relative_dir = r'data\FFL_Info.csv'

with open(relative_dir) as f:
    df = pd.read_csv(f)

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









week = 5
league = 910981
team = 7
html_file = os.path.join('data', str(week), str(league) + '_' + str(team) + '_week' + str(week) + '_0.html')

player = 5
html_file = r'C:\Dev\Python\Projects\FFLStats4\data\1\910981_7_week1_0.html'

soup = Helper.get_soup_file(html_file)
op = parser.get_offensive_player_soup(soup, player)
pd = op.find_all('td')
info = parser.parse_offensive_player(op)



data_manager.quick_export()



kp = parser.get_kicker_player_soup(soup)
pdk = kp.find_all('td')


url = 'https://football.fantasysports.yahoo.com/f1/910981/7/team?&week=5'
soup = Helper.get_soup_url(url)
op0_wk5 = parser.get_offensive_player_soup(soup, 0)
pd_wk5 = op0_wk5.find_all('td')
wk5_info = parser.parse_offensive_player(op0_wk5)

week = 4
league = 910981
team = 7
html_file = os.path.join('data', str(week), str(league) + '_' + str(team) + '_week' + str(week) + '_0.html')
soup = Helper.get_soup_file(html_file)
op0_wk4 = parser.get_offensive_player_soup(soup, 0)
pd_wk4 = op0_wk4.find_all('td')
wk4_info = parser.parse_offensive_player(op0_wk4)



for x in range(10):
    print('Cell: ' + str(x))
    print(pd_wk4[x])
    print('\n')
    print(pd_wk5[x])
    print('\n')
    print('\n')




offensive_player_table = soup.find_all('table', id='statTable0')
op = offensive_player_table[0].find('tbody').find_all('tr')
op0 = op[0]

op_data = parser.parse_offensive_player(op[2])
#print(op_data)

data_soup = op[1].find_all('td')
position = data_soup[0].contents[0].find_all('span')[0].contents[0]
score = data_soup[6].contents[0].contents[0].contents[0]
projected_score = data_soup[7].contents[0].contents[0]
percent_start = data_soup[8].contents[0].contents[0].strip('%')
return_data = [position, score, projected_score, percent_start]
data_soup[1].find_all('a', class_='Nowrap name F-link')
data_soup[1].find_all('span', class_='Fz-xxs')[0].contents[0].split('-')[1]

kicker_table = soup.find_all('table', id='statTable1')
row_soup = kicker_table[0]
data_soup = row_soup.find_all('td')