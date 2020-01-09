import configparser
from datetime import datetime
import math
from data_vis.LeagueVisGen import *
from models.League import League


config = configparser.ConfigParser()
config.read('config.ini')

start_week = config['Season']['StartWeek']

dt = datetime.strptime(start_week, '%m/%d/%y')
td = datetime.today()
elapsed = td - dt
current_week = math.floor(elapsed.days/7)

AFC_id = config['AFC']['id']
NFC_id = config['AFC']['id']

AFC = League(AFC_id, 'AFC')
NFC = League(NFC_id, 'NFC')

AFC.update(current_week)
NFC.update(current_week)


plot_cum_real_score_by_week(AFC)
plot_player_breakdown_for_all_teams(AFC)




