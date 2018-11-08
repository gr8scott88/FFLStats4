import pandas as pd
import os
import requests
import Helper
import DATACONTRACT


class DataManager:
    def __init__(self):
        self.team_score_frame = pd.DataFrame(columns=DATACONTRACT.TEAMSCORECOLS)
        self.player_score_frame = pd.DataFrame(columns=DATACONTRACT.PLAYERSCORECOLS)
        self.league_info_frame = pd.DataFrame(columns=DATACONTRACT.TEAMINFOCOLS)

        self.data_folder = 'data'
        self.league_data_file = 'FFL_Info.csv'

        self.data_file_path = os.path.join(self.data_folder, self.league_data_file)
        self.data_directory = os.path.join(self.data_folder)

        self.league_tracker_frame = self.load_tracker_info()

    def add_team_from_row(self, team_row):
        # print(team_row)
        self.team_score_frame.loc[len(self.team_score_frame)] = team_row

    def add_player_frame(self, player_frame):
        self.player_score_frame.append(player_frame)

    def add_league_info(self, league_info_df):
        self.league_info_frame = league_info_df

    def add_tracker_info(self, tracker_array):
        print(tracker_array)
        for row in tracker_array:
            self.league_tracker_frame.loc[len(self.league_tracker_frame)] = row

    def add_player_from_row(self, player_row):
        # print(player_row)
        self.player_score_frame.loc[len(self.player_score_frame)] = player_row

    def load_tracker_info(self):
        league_info = pd.read_csv(self.data_file_path)
        print(league_info)
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
            url = self.gen_url(unique_id)
            page = requests.get(url)
            self.save_html(save_file, page.content)
            print('Loading from website')
            print(url)
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
        save_name = str(unique_id.league_id) + '_' + str(unique_id.team_id) + '_week' + str(unique_id.week) + '_' + str(unique_id.time) + '.html'
        return save_name

    @staticmethod
    def gen_url(unique_id):
        parse_url = 'https://football.fantasysports.yahoo.com/f1/' + str(unique_id.league) + '/' + str(unique_id.team) + '/' + 'team?&week=' + str(unique_id.week)
        return parse_url

    def get_team_data(self):
        return self.team_score_frame

    def get_player_data(self):
        return self.player_score_frame

    def export_team_data(self, name):
        self.team_score_frame.to_csv(name)

    def export_player_data(self, name):
        self.player_score_frame.to_csv(name)

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

    def export_weekly_team_data(self, week):
        pass

    def add_team_info(self, team_info_array, unique_info):
        full_team_data = unique_info + team_info_array
        self.add_team_from_row(full_team_data)

    def add_player_info(self, player_info_array, unique_info):
        for row in player_info_array:
            full_player_data = unique_info + row
            self.add_player_from_row(full_player_data)

    def cum_sum_position_by_week(self, pos: str, week: int):
        weekly_players = self.player_score_frame.loc[pd['Week'] == week]
        weekly_players_by_pos = weekly_players.loc[weekly_players['ActivePos'] == pos]
        result = weekly_players_by_pos.groupby(['LeagueID', 'TeamID']).sum()
        return result

    def max_score_position_by_week(self, pos: str, week: int):
        weekly_players = self.player_score_frame.loc[pd['Week'] == week]
        weekly_players_by_pos = weekly_players.loc[weekly_players['ActivePos'] == pos]
        result = weekly_players_by_pos.groupby(['LeagueID', 'TeamID']).max()
        return result[['TeamName', 'RealScore']]

    def get_complete_team_frame(self):
        # merged = pd.merge(league.data_manager.team_score_frame,
        # league.data_manager.league_tracker_frame, on='UniqueID')
        merged = pd.merge(self.team_score_frame, self.league_tracker_frame, on='UniqueID')
        return merged

    def export_complete_team_frame(self, league):
        quick_league_file = os.path.join(self.data_directory, str(league) + '_TeamData.csv')
        if os.path.isfile(quick_league_file):
            os.remove(quick_league_file)
        complete_team_frame = self.get_complete_team_frame()
        sorted_team_data = complete_team_frame.sort_values(by=['Week', 'Order'])
        # complete_team_frame.sort_values(by=['Order', 'Week'])
        print('Exporting team info to ' + str(quick_league_file))
        sorted_team_data.to_csv(quick_league_file)
