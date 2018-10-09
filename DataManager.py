import pandas as pd
import os
import requests
import Helper


class DataManager:
    def __init__(self, default_local_dir=None):
        team_columns = ['League', 'Team', 'Week', 'Time', 'RealScore', 'ProjScore']
        self.team_frame = pd.DataFrame(columns=team_columns)

        player_columns = ['League', 'Team', 'Week', 'Time', 'Name', 'PlayerPos', 'ActivePos', 'RealScore', 'ProjScore', 'PctPlayed']
        self.player_frame = pd.DataFrame(columns=player_columns)

        self.local_dir = self.set_local_dir(default_local_dir)

        self.data_folder = 'data'
        self.league_data_file = 'FFL_Info.csv'

        self.data_file_path = os.path.join(self.local_dir, self.data_folder, self.league_data_file)
        self.data_directory = os.path.join(self.local_dir, self.data_folder)

    def add_team_frame(self, team_frame):
        self.team_frame.append(team_frame)

    def add_team_from_row(self, team_row):
        self.team_frame.loc[len(self.team_frame)] = team_row

    def add_player_frame(self, player_frame):
        self.player_frame.append(player_frame)

    def add_player_from_row(self, player_row):
        self.player_frame.loc[len(self.player_frame)] = player_row

    @staticmethod
    def set_local_dir(default_dir):
        try:
            script_path = os.path.dirname(os.path.realpath(__file__))
        except Exception as e:
            if default_dir is not None:
                script_path = default_dir
            else:
                script_path = 'NA'
                print('Must provide a default script path')
        return script_path

    def get_league_info_directory(self) -> str:
        return self.data_file_path

    def get_league_attributes(self):
        league_info = pd.read_csv(self.data_file_path)
        return league_info

    @staticmethod
    def does_file_exist(file_path):
        if os.path.isfile(file_path):
            return True
        else:
            return False

    def load_or_download_html(self, unique_id: Helper.UniqueID):
        save_file = self.get_save_file_path(unique_id)
        print('Save file: ' + save_file)

        if self.does_file_exist(save_file):
            with open(save_file) as f:
                print('Opening saved file')
                return f.read()
        else:
            page = requests.get(self.gen_url(unique_id))
            self.save_html(save_file, page.content)
            print('Loading from website')
            return page.content

    @staticmethod
    def save_html(file_path, html):
        with open(file_path, 'wb') as f:
            f.write(str(html).encode('utf-8'))

    def get_save_file_path(self, unique_id: Helper.UniqueID):
        directory = self.get_folder_path(unique_id)
        self.create_directory_if_necessary(directory)
        return os.path.join(directory, self.get_file_name(unique_id))

    def get_folder_path(self, unique_id: Helper.UniqueID):
        return os.path.join(self.local_dir, 'data', str(unique_id.week))

    @staticmethod
    def get_file_name(unique_id: Helper.UniqueID):
        save_name = str(unique_id.league) + '_' + str(unique_id.team) + '_week' + str(unique_id.week) + '_' + str(unique_id.time) + '.html'
        return save_name

    @staticmethod
    def gen_url(unique_id):
        parse_url = 'https://football.fantasysports.yahoo.com/f1/' + str(unique_id.league) + '/' + str(unique_id.team) + '/' + 'team?&week=' + str(unique_id.week)
        return parse_url

    def get_team_data(self):
        return self.team_frame

    def get_player_data(self):
        return self.player_frame

    def export_team_data(self, name):
        self.team_frame.to_csv(name)

    def export_player_data(self, name):
        self.player_frame.to_csv(name)

    def quick_export(self):

        quick_team_file = os.path.join(self.data_directory, 'team.csv')
        quick_player_file = os.path.join(self.data_directory, 'player.csv')
        if os.path.isfile(quick_team_file):
            os.remove(quick_team_file)
        self.export_team_data(quick_team_file)

        if os.path.isfile(quick_player_file):
            os.remove(quick_player_file)
        self.export_player_data(quick_player_file)

    @staticmethod
    def create_directory_if_necessary(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)