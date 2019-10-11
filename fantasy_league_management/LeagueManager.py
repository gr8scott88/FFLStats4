from utility.DateManager import DateManager
import configparser
import os
from utility.YahooWebHelper import YahooWebHelper
from web_parsing.LeaguePageParser import LeaguePageParser
import pandas as pd

class LeagueManager:
    def __init__(self, league_id):
        self.league_id = league_id
        self.team_ids = []
        self.date_manager = DateManager()
        self.generate_league()
        self.web_helper = YahooWebHelper()


    def load_league(self):
        config_file = f'config/{self.league_id}.ini'
        if os.path.isfile(config_file):
            self.load_team_ids()
        pass


    def generate_league(self):
        config_file = f'config/{self.league_id}.ini'
        if os.path.isfile(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            for team in config['TEAMS'].values():
                self.team_ids.append(team)
        else:
            parser = LeaguePageParser(self.league_id, self.web_helper)
            df = parser.parse_league_info()


    def convert_df_to_league_config(self, df: pd.DataFrame):
        pass

    def load_team_ids(self, path):
        with open(path) as configfile:


    def parse_all_data(self):
        current_week = self.date_manager.get_current_week()
        for week in range(current_week):

    def parse_league_by_week(self, week):
        pass



# class MultiLeagueManager:
#     def __init__(self, league_config: configparser):
#         self.league_ids = []
#         self.leagues = []
#         self.config = league_config
#         self.load_league_ids()
#
#     def load_league_ids(self):
#         leagues = []
#         for key in self.config['LEAGUES']:
#             if 'league' in key:
#                 leagues.append(self.config['LEAGUES'][key])
#         self.league_ids = leagues
#
#     def load_leagues(self):
#         for league_id in self.league_ids:
#             league = LeagueManager(league_id)
#             # league.parse_all_data()
#             self.leagues.append(league)
#
#     def load_league_by_week(self, week):
#         pass
#
#     def load_all_data_to_date(self):
#         for league in self.leagues:
#             league.lo
