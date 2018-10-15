import DataParser as dp
import LeagueParser as lp
import GLOBALS
import os
import pandas as pd
import FileManager



class League:
    def __init__(self, league_id):
        self.league_id = league_id
        # self.parser = dp.DataParser()
        self.parser = lp.LeagueParser()
        self.load_league_info()
        self.league_info = []

    def load_league_info(self):
        league_dir = os.path.join(GLOBALS.ROOTDIR, str(self.league_id))
        file_name = str(self.league_id) + '_info.csv'
        league_info = FileManager.load_df(league_dir, file_name)
        if not league_info:
            league_info = self.parser.parse_league_info(self.league_id)
            FileManager.save_df_to_file(league_dir, file_name, league_info)
        print(league_info)
        self.league_info = league_info

    def load_all_season_data(self, current_week):
        pass

    def load_single_week_data(self, week_id):
        pass


'''
  all_league_data = []

        for index, row in league_info.iterrows():
            team_id = row['TeamId']
            league_id = row['LeagueId']
            team_name = row['Team']
            team_order = row['Order']
            league_name = row['LeagueName']
            unique_id = Helper.UniqueID(league_id, league_name, team_id, team_name, team_order, week_id)
            print('Parsing team: ' + str(league_name) + r' / ' + str(team_name)+ '(' + str(league_id) + r'/' + str(team_id) + ')')
            all_data_for_team = self.team_manager.get_team_info(unique_id)

            all_league_data.append(all_data_for_team)
            # print(all_data_for_team)

        for team in all_league_data:
            team_row = team[0] + team[1]
            self.data_manager.add_team_from_row(team_row)
            player_array = team[2]
            for player in player_array:
                player_row = team[0] + player
                self.data_manager.add_player_from_row(player_row)
'''