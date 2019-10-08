from models import Webpage
import GLOBALS
import os

class LocalDataManager:
    def __init__(self):
        pass

    def save_team_html(self, league_id, team_id, page: Webpage):
        folder = gen_folder_path([league_id, 'Team Info'])
        fpath = os.path.join(folder, f'{team_id}.html')
        with open(fpath, 'w') as f:
            f.write(page)

    def save_league_html(self, league_id, page: Webpage):
        folder = gen_folder_path([league_id])
        fpath = os.path.join(folder, f'League_Info.html')
        with open(fpath, 'w') as f:
            f.write(page)

    def save_week_html(self, league_id, team_id, week, page: Webpage):
        folder = gen_folder_path([league_id, week])
        fpath = os.path.join(folder, f'{week}_results.html')
        with open(fpath, 'w') as f:
            f.write(page)

    def load_team_html(self, league_id, team_id):
        folder = gen_folder_path([league_id, 'Team Info'])
        fpath = os.path.join(folder, f'{team_id}.html')
        with open(fpath, 'w') as f:
            #TODO

    def load_league_html(self, league_id):
        folder = gen_folder_path([league_id])
        fpath = os.path.join(folder, f'League_Info.html')
        with open(fpath, 'w') as f:
            #TODO

    def load_week_html(self, league_id, team_id, week):
        folder = gen_folder_path([league_id, week])
        fpath = os.path.join(folder, f'{week}_results.html')
        with open(fpath, 'w') as f:
            #TODO


def gen_folder_path(folders):
    path = r'data_archive'
    for folder in folders:
        path = os.path.join(path, folder)
    return path



