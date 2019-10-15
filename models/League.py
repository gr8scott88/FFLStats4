import pandas as pd
from models import Team, Webpage, DATACONTRACT
from web_parsing.LeaguePageParser import LeaguePageParser
from data_storage.LocalDataManager import LocalDataManager
from data_handlers.PandasHandler import PandasDataHandler
from utility.YahooWebHelper import YahooWebHelper


class League:
    def __init__(self, league_id):
        self.league_id = league_id
        self.league_parser = LeaguePageParser()
        self.web_helper = YahooWebHelper()
        self.local_data_manager = LocalDataManager()
        self.pandas_manager = PandasDataHandler()
        self.league_info = self.load_league_info()
        self.matchup_info = self.load_matchup_info()

    def load_league_info(self) -> pd.DataFrame:
        league_df = self.local_data_manager.load_league_df()
        if not league_df:
            league_soup = self.local_data_manager.load_league_soup(self.league_id)
            if league_soup is False:
                league_soup = self.web_helper.get_league_soup(self.league_id)
            league_df = self.league_parser.parse_league_info(league_soup)
        print('Loaded League Info:')
        print(league_df)
        return league_df

    def load_matchup_info(self) -> pd.DataFrames:
        matchup_df = self.local_data_manager.load_matchup_df()
        if not matchup_df:
            for week in

    def get_team_ids(self):
        #TODO
        pass

    def load_data_point(self, week, time):
        for index, fantasy_player in self.league_info.iterrows():
            print(str(fantasy_player[DATACONTRACT.TEAM_ID]) + r'/' + fantasy_player[str(DATACONTRACT.TEAM_NAME)])
            team_id = fantasy_player[DATACONTRACT.TEAM_ID]
            team = Team.Team(self.league_id, team_id)
            team.load_soup_for_week(week, 0)
            team_data = team.parse_team_info()
            unique_id = str(self.league_id) + '_' + str(team_id)
            self.pandas_manager.add_team_info(team_data, [unique_id, week, time])
            team_player_data = team.parse_all_player_info()
            self.pandas_manager.add_player_info(team_player_data, [unique_id, week, time])

    def load_all_data_points(self, current_week):
        for week in range(current_week):
            print('Parsing week ' + str(current_week+1))
            self.load_data_point(week+1, 0)

    def save_league_data(self):
        teamfilename = str(self.league_id) + '_TeamData'
        self.local_data_manager.export_team_data(teamfilename)
        playerfilename = str(self.league_id) + '_PlayerData'
        self.local_data_manager.export_player_data(playerfilename)
