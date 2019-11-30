from models import Webpage
import os
import pandas as pd
from models import DATACONTRACT


def save_league_html(self, league_id, page: Webpage):
    folder = gen_folder_path([league_id])
    fpath = os.path.join(folder, f'{DATACONTRACT.LEAGUEHTML}.html')
    with open(fpath, 'w') as f:
        f.write(page)


def save_team_html_by_week(league_id, team_id, week, page: Webpage):
    folder = gen_folder_path([league_id, week])
    fpath = os.path.join(folder, f'{team_id}_{DATACONTRACT.TEAMHTML}.html')
    with open(fpath, 'w') as f:
        f.write(page)


def save_matchup_html_by_week(league_id, team_id, week, page: Webpage):
    folder = gen_folder_path([league_id, week])
    fpath = os.path.join(folder, f'{team_id}_{DATACONTRACT.MATCHUPHTML}.html')
    with open(fpath, 'w') as f:
        f.write(page)


def load_league_soup(league_id):
    folder = gen_folder_path([league_id])
    fpath = os.path.join(folder, f'{DATACONTRACT.LEAGUEHTML}.html')
    if not os.path.exists(fpath):
        return False
    get_soup(fpath)


def load_team_soup_by_week(league_id, team_id, week):
    folder = gen_folder_path([league_id, week])
    fpath = os.path.join(folder, f'{team_id}_{DATACONTRACT.TEAMHTML}.html')
    if not os.path.exists(fpath):
        return False
    get_soup(fpath)


def load_matchup_soup_by_week(self, league_id, team_id, week):
    folder = gen_folder_path([league_id, week])
    fpath = os.path.join(folder, f'{team_id}_{DATACONTRACT.MATCHUPHTML}.html')
    if not os.path.exists(fpath):
        return False
    get_soup(fpath)


def save_to_parquet(league_id, data, name, overwrite=False):
    filename = f'{league_id}_{name}.parquet'
    full_file = gen_full_file_path([league_id], filename)
    if os.path.isfile(full_file):
        if overwrite:
            os.remove(full_file)
            data.to_parquet(full_file, compression='gzip')
        else:
            print('File already exists, specify OVERWRITE')
            return False
    else:
        data.to_parquet(full_file, compression='gzip')
    print('Saved to PARQUET file')
    return True


def load_from_parquet(league_id, name):
    filename = f'{league_id}_{name}.parquet'
    full_file = gen_full_file_path([league_id], filename)
    if os.path.isfile(full_file):
        df = pd.read_parquet(full_file)
        print(f'Loaded file {full_file} from saved data')
        return df


def get_league_directory(league_id):
    return os.path.join(DATACONTRACT.DATAROOT, str(league_id))


def gen_filepath(league_id, name):
    directory = os.path.join(DATACONTRACT.DATAROOT, str(league_id), name)
    print(directory)
    return directory


def gen_folder_path(folders):
    path = DATACONTRACT.DATAROOT
    for folder in folders:
        folder_string = str(folder)
        path = os.path.join(path, folder_string)
    return path


def gen_full_file_path(folders, filename):
    path = DATACONTRACT.DATAROOT
    for folder in folders:
        folder_string = str(folder)
        path = os.path.join(path, folder_string)
    path = os.path.join(path, filename)
    return path


def get_soup(fpath):
    with open(fpath, 'r') as f:
        #TODO
        pass

def export_to_csv(data:pd.DataFrame, filename):
    data.to_csv(gen_full_file_path([DATACONTRACT.EXPORTDIR], filename))
