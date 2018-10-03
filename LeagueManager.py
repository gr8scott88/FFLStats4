import sys
import pandas as pd
import os
import TeamManager as tm


def load_league(file_dir, week_id):
    league_dataframe = pd.read_csv(file_dir)

    for index, row in league_dataframe.iterrows():
        team_id = row['TeamId']
        league_id = row['LeagueId']
        all_data = tm.get_team_info(league_id, team_id, week_id)
        print(all_data)

