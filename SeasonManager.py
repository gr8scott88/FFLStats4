import sys
import pandas as pd
import os
import TeamManager as tm
import Objects
import LeagueManager as lm


def load_all_season_data(current_week):
    relative_dir = r'data\FFL_Info.csv'
    # script_dir = r'C:\Users\gr8sc\PycharmProjects\FFLStats4'
    # script_dir = r'C:\Dev\Python\FFLStats4'
    script_dir = r'C:\Dev\Python\Projects\FFLStats4'
    league_info_file_path = os.path.join(script_dir, relative_dir)
    print(league_info_file_path)

    team_columns = ['League', 'Team', 'Week', 'Time', 'RealScore', 'ProjScore']
    team_frame = pd.DataFrame(columns=team_columns)

    player_columns = ['League', 'Team', 'Week', 'Time', 'ActivePos', 'RealScore', 'ProjScore', 'PctPlayed']
    player_frame = pd.DataFrame(columns=player_columns)

    for week in range(current_week):
        week_id = week + 1
        [weekly_team_frame, weekly_player_frame] = lm.load_league(league_info_file_path, week_id)
        team_frame.append(weekly_team_frame)
        player_frame.append(weekly_player_frame)

    return [team_frame, player_frame]


def load_single_week_data(week_id):
    relative_dir = r'data\FFL_Info.csv'
    # script_dir = r'C:\Users\gr8sc\PycharmProjects\FFLStats4'
    # script_dir = r'C:\Dev\Python\FFLStats4'
    script_dir = r'C:\Dev\Python\Projects\FFLStats4'
    league_info_file_path = os.path.join(script_dir, relative_dir)
    print(league_info_file_path)

    team_columns = ['League', 'Team', 'Week', 'Time', 'RealScore', 'ProjScore']
    team_frame = pd.DataFrame(columns=team_columns)

    player_columns = ['League', 'Team', 'Week', 'Time', 'ActivePos', 'RealScore', 'ProjScore', 'PctPlayed']
    player_frame = pd.DataFrame(columns=player_columns)

    [weekly_team_frame, weekly_player_frame] = lm.load_league(league_info_file_path, week_id)
    team_frame.append(weekly_team_frame)
    player_frame.append(weekly_player_frame)

    return [team_frame, player_frame]

