from models import Webpage
import os
import pandas as pd


class LocalDataManager:
    def __init__(self):
        self.league_data = 'leagueInfo'
        self.team_data = 'teamData'
        self.matchup_data = 'matchupData'

    def save_league_html(self, league_id, page: Webpage):
        folder = gen_folder_path([league_id])
        fpath = os.path.join(folder, f'{self.league_data}.html')
        with open(fpath, 'w') as f:
            f.write(page)

    def save_team_html_by_week(self, league_id, team_id, week, page: Webpage):
        folder = gen_folder_path([league_id, week])
        fpath = os.path.join(folder, f'{team_id}_{self.team_data}.html')
        with open(fpath, 'w') as f:
            f.write(page)

    def save_matchup_html_by_week(self, league_id, team_id, week, page: Webpage):
        folder = gen_folder_path([league_id, week])
        fpath = os.path.join(folder, f'{team_id}_{self.matchup_data}.html')
        with open(fpath, 'w') as f:
            f.write(page)

    def load_league_soup(self, league_id):
        folder = gen_folder_path([league_id])
        fpath = os.path.join(folder, f'{self.league_data}.html')
        if not os.path.exists(fpath):
            return False
        self.get_soup(fpath)

    def load_league_df(self, league_id):
        try:
            folder = gen_folder_path([league_id])
            fpath = os.path.join(folder, f'{self.league_data}.csv')
            df = pd.read_csv(fpath)
            return df
        except Exception as e:
            return False

    def load_team_soup_by_week(self, league_id, team_id, week):
        folder = gen_folder_path([league_id, week])
        fpath = os.path.join(folder, f'{team_id}_{self.team_data}.html')
        if not os.path.exists(fpath):
            return False
        self.get_soup(fpath)

    def load_matchup_df(self, league_id):
        #TODO
        return False

    def load_matchup_soup_by_week(self, league_id, team_id, week):
        folder = gen_folder_path([league_id, week])
        fpath = os.path.join(folder, f'{team_id}_{self.matchup_data}.html')
        if not os.path.exists(fpath):
            return False
        self.get_soup(fpath)

    @staticmethod
    def get_soup(fpath):
        with open(fpath, 'r') as f:
            #TODO
            pass

    # def save_week_html(self, league_id, team_id, week, page: Webpage):
    #     folder = gen_folder_path([league_id, week])
    #     fpath = os.path.join(folder, f'{week}_results.html')
    #     with open(fpath, 'w') as f:
    #         f.write(page)
    #
    # def load_team_html(self, league_id, team_id):
    #     folder = gen_folder_path([league_id, 'Team Info'])
    #     fpath = os.path.join(folder, f'{team_id}.html')
    #     with open(fpath, 'w') as f:
    #         #TODO
    #         pass


def gen_folder_path(folders):
    path = r'data_archive'
    for folder in folders:
        path = os.path.join(path, folder)
    return path



