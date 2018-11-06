import LeagueParser as lp
import GLOBALS
import os
import FileManager
import DATACONTRACT
import WebHelper
import Webpage
import pandas as pd
import Team
import DataManager


class League:
    def __init__(self, league_id, data_manager):
        self.league_id = league_id
        self.parser = lp.LeagueParser()
        self.league_info = self.load_league_info()
        # self.data_manager = DataManager.DataManager()
        self.data_manager = data_manager
        self.data_manager.add_league_info(self.league_info)

    def load_league_info(self) -> pd.DataFrame:
        league_dir = os.path.join(GLOBALS.ROOTDIR, str(self.league_id))
        print(league_dir)
        file_name = str(self.league_id) + '_info.csv'
        print(file_name)
        league_info = FileManager.load_df(league_dir, file_name)
        # print(league_info)
        if league_info is False:
            league_url = WebHelper.build_url(GLOBALS.URLROOT, str(self.league_id))
            print('Loading league info from:')
            print(league_url)
            webpage = Webpage.Webpage(league_url)
            league_info = self.parser.parse_league_info(webpage.get_soup())
            # df = DataFrame(table, columns=headers)
            league_info = pd.DataFrame(league_info, DATACONTRACT.LEAGUEINFOCOLS)
            FileManager.save_df_to_file(league_dir, file_name, league_info)
        print('Loaded League Info:')
        print(league_info)
        # self.league_info = league_info
        return league_info

    def load_all_season_data(self, current_week):
        for week in range(current_week):
            self.load_single_week_data(week+1)

    def load_single_week_data(self, week_id):
        for index, fantasy_player in self.league_info.iterrows():
            print(str(fantasy_player[DATACONTRACT.TEAM_ID]) + r'/' + fantasy_player[str(DATACONTRACT.TEAM_NAME)])
            team_id = fantasy_player[DATACONTRACT.TEAM_ID]
            team = Team.Team(self.league_id, team_id)
            team.load_soup_for_week(week_id, 0)
            team_data = team.parse_team_info()
            unique_id = str(self.league_id) + '_' + str(team_id)
            self.data_manager.add_team_info(team_data, unique_id)
            team_player_data = team.parse_all_player_info()
            self.data_manager.add_player_info(team_player_data, unique_id)

    def load_data_point(self, week, time):
        for index, fantasy_player in self.league_info.iterrows():
            print(str(fantasy_player[DATACONTRACT.TEAM_ID]) + r'/' + fantasy_player[str(DATACONTRACT.TEAM_NAME)])
            team_id = fantasy_player[DATACONTRACT.TEAM_ID]
            team = Team.Team(self.league_id, team_id)
            team.load_soup_for_week(week, 0)
            team_data = team.parse_team_info()
            unique_id = str(self.league_id) + '_' + str(team_id)
            self.data_manager.add_team_info(team_data, [unique_id, week, time])
            team_player_data = team.parse_all_player_info()
            self.data_manager.add_player_info(team_player_data, [unique_id, week, time])

    def load_all_data_points(self, current_week):
        for week in range(current_week):
            print('Parsing week ' + str(current_week+1))
            self.load_data_point(week+1, 0)
