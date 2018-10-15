import os
import pandas as pd


def save_df_to_file(directory, name, df: pd.DataFrame, overwrite=True):
    save_file = os.path.join(directory, name)
    if overwrite:
        delete_file(save_file)
    df.to_csv(save_file)


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def load_df(directory, name):
    df = False
    try:
        df = pd.read_csv(os.path.join(directory, name))
    except Exception as e:
        print('DF does not exist')
    return df


def save_html(directory, name, html, overwrite=True):
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
