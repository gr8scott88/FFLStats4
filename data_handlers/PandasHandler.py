import os
import pandas as pd


class PandasDataHandler:
    def __init__(self):
        pass

    @staticmethod
    def load_local_league_info(league_id) -> pd.DataFrame:
        load_file = f'{league_id}_LeagueInfo.parquet'
        if os.path.isfile(load_file):
            df = pd.read_parquet(load_file)
            print(f'Loaded file {load_file} from saved data')
            return df

    @staticmethod
    def save_local_league_info(league_id, league_data, overwrite=False):
        save_file = f'{league_id}_LeagueInfo.parquet'
        if os.path.isfile(save_file):
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

    @staticmethod
    def load_local_team_weekly_scores(league_id):
        load_file = f'{league_id}_WeeklyTeamScores.parquet'
        if os.path.isfile(load_file):
            df = pd.read_parquet(load_file)
            print(f'Loaded file {load_file} from saved data')
            return df

    @staticmethod
    def save_local_team_weekly_scores(league_id, weekly_score_data, overwrite=False):
        save_file = f'{league_id}_WeeklyTeamScores.parquet'
        if os.path.isfile(save_file):
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

