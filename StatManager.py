import pandas as pd
import matplotlib
import DataManager

class StatManager:
    def __init__(self, data_manager: DataManager):
        self.team_frame = data_manager.team_frame
        self.player_frame = data_manager.player_frame

    def plot_real_score_by_week(self):
        team_stats = self.player_frame.groupby(['League', 'Team'])
        team_stats.plot('Real Score')

    def cum_sum_position_by_week(self, pos: str, week: int):
        weekly_players = self.player_frame.loc[self.player_frame['Week'] == week]
        weekly_players_by_pos = weekly_players.loc[weekly_players['ActivePos'] ==  pos]
        # result = weekly_players_by_pos.groupby(['LeagueID', 'TeamID', 'TeamOrder']).sum()
        result = weekly_players_by_pos.groupby(['LeagueName', 'TeamName', 'TeamOrder']).sum()
        # sorted_results = result.sort_values(['LeagueID', 'TeamOrder'])
        sorted_results = result.sort_values(['LeagueName', 'TeamOrder'])
        return sorted_results['RealScore']

    def max_score_position_by_week(self, pos: str, week: int):
        weekly_players = self.player_frame.loc[self.player_frame['Week'] == week]
        weekly_players_by_pos = weekly_players.loc[weekly_players['ActivePos'] == pos]
        # result = weekly_players_by_pos.groupby(['LeagueID', 'TeamID', 'TeamOrder']).max()
        result = weekly_players_by_pos.groupby(['LeagueName', 'TeamName', 'TeamOrder']).max()
        # return result[['TeamName', 'RealScore']]
        # sorted_results = result.sort_values(['LeagueID','TeamOrder'])
        sorted_results = result.sort_values(['LeagueName', 'TeamOrder'])
        return sorted_results['RealScore']
