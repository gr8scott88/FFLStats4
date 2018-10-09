import SeasonManager as sm
import DataManager as dm
import DataParser as dp
import Helper
import StatManager as stat
import matplotlib as plt



script_dir = r'C:\Users\gr8sc\PycharmProjects\FFLStats4'

data_manager = dm.DataManager(script_dir)
season_manager = sm.SeasonManager(data_manager)

season_manager.load_all_season_data(4)

data_manager.quick_export()







season_manager.load_single_week_data(4)

soup = Helper.get_soup_url('https://football.fantasysports.yahoo.com/f1/910981/9/team?&week=4')

parser = dp.DataParser()

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