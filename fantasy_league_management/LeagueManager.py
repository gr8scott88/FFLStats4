from utility.DateManager import DateManager
import configparser
import os


class LeagueManager:
    def __init__(self, league_id):
        self.league_id = league_id
        self.team_ids = []
        self.date_manager = DateManager()
        self.generate_league()

    def generate_league(self):
        config_file = f'config/{self.league_id}.ini'
        if os.path.isfile(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            for team in config['TEAMS'].values():
                self.team_ids.append(team)
        else:


    def load_team_ids(self):
        with open(f'config/{self.league_id}.ini', 'w') as configfile:


    def parse_all_data(self):
        current_week = self.date_manager.get_current_week()


class MultiLeagueManager:
    def __init__(self, league_config: configparser):
        self.league_ids = []
        self.leagues = []
        self.config = league_config

    def load_league_ids(self):
        leagues = []
        for key in self.config['LEAGUES']:
            if 'league' in key:
                leagues.append(self.config['LEAGUES'][key])
        self.league_ids = leagues

    def load_leagues(self):
        for league_id in self.league_ids:
            league = LeagueManager(league_id)
            league.parse_all_data()
            self.leagues.append(league)