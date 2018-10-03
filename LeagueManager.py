import sys
import pandas as pd
import os
import TeamManager as tm
import Objects


def load_league(league_info_file_path, week_id):
    league_info = pd.read_csv(league_info_file_path)

    all_league_data = []

    team_columns = ['League', 'Team', 'Week', 'Time', 'RealScore', 'ProjScore']
    team_frame = pd.DataFrame(columns=team_columns)

    player_columns = ['League', 'Team', 'Week', 'Time', 'ActivePos', 'RealScore', 'ProjScore', 'PctPlayed']
    player_frame = pd.DataFrame(columns=player_columns)

    for index, row in league_info.iterrows():
        team_id = row['TeamId']
        league_id = row['LeagueId']
        # all_data_for_team = tm.get_team_info(league_id, team_id, week_id)
        unique_id = Objects.UniqueID(league_id, team_id, week_id)
        all_data_for_team = tm.get_team_info(unique_id)

        # data_with_id =
        all_league_data.append(all_data_for_team)
        print(all_data_for_team)

    for team in all_league_data:
        team_row = team[0] + team[1]
        team_frame.loc[len(team_frame)] = team_row
        player_array = team[2]
        for player in player_array:
            player_row = team[0] + player
            player_frame.loc[len(team_frame)] = player_row

    return [team_frame, player_frame]

