import os
import pandas as pd
from archive import GLOBALS


def save_df_to_file(directory, name, df: pd.DataFrame, overwrite=True):
    if not does_directory_exist(directory):
        create_directory(directory)
    save_file = os.path.join(directory, name)
    if overwrite:
        delete_file(save_file)
    df.to_csv(save_file)


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def load_league_info(league_id):
    league_dir = os.path.join(GLOBALS.ROOTDIR, str(league_id))
    file_name = str(league_id) + '_info.csv'


def load_df(directory, name):
    df = False
    try:
        df = pd.read_csv(os.path.join(directory, name))
    except Exception as e:
        print('DF does not exist')
    return df


def save_html(directory, name, html, overwrite=True):
    if not does_directory_exist(directory):
        create_directory(directory)
    save_file = os.path.join(directory, name)
    if overwrite:
        delete_file(save_file)
    with open(save_file, 'wb') as file:
        file.write(str(html).encode('utf-8'))


def does_file_exist(file_path):
    if os.path.isfile(file_path):
        return True
    else:
        return False


def does_directory_exist(directory):
    if os.path.isdir(directory):
        return True
    else:
        return False


def create_directory(directory):
    os.mkdir(directory)


def load_html(directory, file):
    html_file = os.path.join(directory, file)
    if not does_file_exist(html_file):
        return False
    else:
        with open(html_file) as f:
            # print('Opening saved html file')
            return f.read()


# def get_html_file(league, team, week)