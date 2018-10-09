import pandas as pd
import matplotlib


class StatManager:
    def __init__(self, team_frame: pd.DataFrame, player_frame: pd.DataFrame):
        self.team_frame = team_frame
        self.player_frame = player_frame

    def cum_sum_WR(self):
        pass

    def real_score_by_week(self):
        team_stats = self.player_frame.groupby(['League', 'Team'])
        team_stats.plot('Real Score')
