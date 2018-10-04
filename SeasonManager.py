import sys
import pandas as pd
import os
import TeamManager as tm
import Helper
import LeagueManager as lm
import DataManager


class SeasonManager:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.league_manager = lm.LeagueManager(data_manager)

    def load_all_season_data(self, current_week):
        for week in range(current_week):
            week_id = week + 1
            print('Parsing week ' + str(week_id))
            self.league_manager.load_league(week_id)

    def load_single_week_data(self, week_id):
        self.league_manager.load_league(week_id)
