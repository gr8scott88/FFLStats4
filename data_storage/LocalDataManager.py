from models import Webpage
import os
import pandas as pd


data_root = 'data_archive'


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

    def load_local_league_info(self, league_id) -> pd.DataFrame:
        load_file = f'{league_id}_LeagueInfo.parquet'
        if os.path.isfile(self.gen_filepath(league_id, load_file)):
            df = pd.read_parquet(load_file)
            print(f'Loaded file {load_file} from saved data')
            return df

    def save_local_league_info(self, league_id, league_data, overwrite=False):
        save_file = f'{league_id}_LeagueInfo.parquet'
        if os.path.isfile(self.gen_filepath(league_id, save_file)):
            if overwrite:
                os.remove(save_file)
                league_data.to_parquet(save_file, compression='gzip')
            else:
                print('File already exists, specify OVERWRITE')
                return False
        else:
            league_data.to_parquet(save_file, compression='gzip')
        print('Saved to PARQUET file')
        return True

    def load_local_team_weekly_scores(self, league_id):
        load_file = f'{league_id}_WeeklyTeamScores.parquet'
        if os.path.isfile(self.gen_filepath(league_id, load_file)):
            df = pd.read_parquet(load_file)
            print(f'Loaded file {load_file} from saved data')
            return df

    def save_local_team_weekly_scores(self, league_id, weekly_score_data, overwrite=False):
        save_file = f'{league_id}_WeeklyTeamScores.parquet'
        if os.path.isfile(self.gen_filepath(league_id, save_file)):
            if overwrite:
                os.remove(save_file)
                weekly_score_data.to_parquet(save_file, compression='gzip')
            else:
                print('File already exists, specify OVERWRITE')
                return False
        else:
            weekly_score_data.to_parquet(save_file, compression='gzip')
        print('Saved to PARQUET file')
        return True

    def load_local_weekly_matcups(self, league_id):
        load_file = f'{league_id}_WeeklyMatchups.parquet'
        if os.path.isfile(self.gen_filepath(league_id, load_file)):
            df = pd.read_parquet(load_file)
            print(f'Loaded file {load_file} from saved data')
            return df

    def save_local_weekly_matchups(self, league_id, weekly_matchup_data, overwrite=False):
        save_file = f'{league_id}_WeeklyMatchups.parquet'
        if os.path.isfile(self.gen_filepath(league_id, save_file)):
            if overwrite:
                os.remove(save_file)
                weekly_matchup_data.to_parquet(save_file, compression='gzip')
            else:
                print('File already exists, specify OVERWRITE')
                return False
        else:
            weekly_matchup_data.to_parquet(save_file, compression='gzip')
        print('Saved to PARQUET file')
        return True

    def save_to_parquet(self, league_id, data, name, overwrite=False):
        save_file = f'{league_id}_{name}.parquet'
        full_file = self.gen_filepath(league_id, save_file)
        if os.path.isfile(full_file):
            if overwrite:
                os.remove(full_file)
                data.to_parquet(save_file, compression='gzip')
            else:
                print('File already exists, specify OVERWRITE')
                return False
        else:
            data.to_parquet(full_file, compression='gzip')
        print('Saved to PARQUET file')
        return True

    def load_from_parquet(self, league_id, name):
        load_file = f'{league_id}_{name}.parquet'
        full_file = self.gen_filepath(league_id, load_file)
        if os.path.isfile(full_file):
            df = pd.read_parquet(full_file)
            print(f'Loaded file {full_file} from saved data')
            return df

    @staticmethod
    def get_league_directory(league_id):
        return os.path.join(data_root, str(league_id))

    def gen_filepath(self, league_id, name):
        directory = os.path.join(data_root, str(league_id), name)
        print(directory)
        return directory

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



