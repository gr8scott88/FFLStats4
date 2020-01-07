import configparser
from models import League
from data_vis.LeagueVisualizer import LeagueVisualizer


config = configparser.ConfigParser()
config.read('config.ini')

start_week = config['Season']['StartWeek']

AFC_id = config['AFC']['id']
NFC_id = config['AFC']['id']

load_thru_week = 12

AFC = League.League(AFC_id, 'AFC')
NFC = League.League(NFC_id, 'NFC')



