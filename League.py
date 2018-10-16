import LeagueParser as lp
import GLOBALS
import os
import FileManager
import DATACONTRACT
import WebHelper
import Webpage
import pandas as pd


class League:
    def __init__(self, league_id):
        self.league_id = league_id
        self.parser = lp.LeagueParser()
        self.league_info = self.load_league_info()

    def load_league_info(self):
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
            FileManager.save_df_to_file(league_dir, file_name, league_info)
        print(league_info)
        # self.league_info = league_info
        return league_info

    def load_all_season_data(self, current_week):
        for week in range(current_week):
            self.load_single_week_data(week+1)

    def load_single_week_data(self, week_id):
        for index, player in self.league_info.iterrows():
            print(str(player[DATACONTRACT.TEAM_ID]) + r'/' + player[str(DATACONTRACT.TEAM_NAME)])
