import pandas as pd
from models import Team, Webpage, DATACONTRACT
from web_parsing.LeaguePageParser import LeaguePageParser
from web_parsing.MatchPageParser import MatchParser
from web_parsing.TeamPageParser import TeamParser
from data_storage.LocalDataManager import LocalDataManager
from data_handlers.PandasHandler import PandasDataHandler
from utility.YahooWebHelper import YahooWebHelper


total_weeks = 16
current_week = 7


class League:
    def __init__(self, league_id):
        self.league_id = league_id
        self.league_parser = LeaguePageParser()
        self.match_parser = MatchParser()
        self.team_parser = TeamParser()
        self.web_helper = YahooWebHelper()
        self.local_data_manager = LocalDataManager()
        self.pandas_manager = PandasDataHandler()
        self.league_info = self.load_league_info()
        self.matchup_info = self.load_matchup_info()
        self.scores_df = None

    def load_league_info(self) -> pd.DataFrame:
        # league_df = self.local_data_manager.load_local_league_info(self.league_id)
        league_df = self.local_data_manager.load_from_parquet(self.league_id, "LeagueInfo")
        if league_df is None:
            # league_soup = self.local_data_manager.load_league_soup(self.league_id)
            # if league_soup is False:
            league_soup = self.web_helper.get_league_soup(self.league_id)
            league_df = self.league_parser.parse_league_info(league_soup)
            print('Loaded League Info from WEB')
            # self.local_data_manager.save_local_league_info(self.league_id, league_df, False)
            self.local_data_manager.save_to_parquet(self.league_id, league_df, "LeagueInfo", False)
        else:
            print('Loaded League Info from PARQUET file')
        # print(league_df)
        return league_df

    def load_matchup_info(self) -> pd.DataFrame:
        # matchup_df = self.local_data_manager.load_local_weekly_matcups(self.league_id)
        matchup_df = self.local_data_manager.load_from_parquet(self.league_id, "MatchupInfo")
        if matchup_df is None:
            matchup_array = []
            for index, team_row in self.league_info.iterrows():
                team_id = team_row['TeamID']
                team_name = team_row['TeamName']
                team_matchups = []
                for week in range(total_weeks):
                    match_page_soup = self.web_helper.get_team_soup_by_week(self.league_id, team_id, week+1)
                    weekly_matchup = self.team_parser.get_weekly_opponent(match_page_soup)
                    print(f'{team_id} vs {weekly_matchup}')
                    team_matchups.append(weekly_matchup)
                matchup_row = [team_id, team_name]
                matchup_row.extend(team_matchups)
                matchup_array.append(matchup_row)
            matchup_df = self.gen_matchup_df(matchup_array)
            # self.local_data_manager.save_local_weekly_matchups(self.league_id, matchup_df, False)
            self.local_data_manager.save_to_parquet(self.league_id, matchup_df, "MatchupInfo", False)
            print('Loaded Matchup Info from WEB')
        else:
            print('Loaded Matchup Info from PARQUET file')
        return matchup_df

    @staticmethod
    def gen_matchup_df(matchup_array) -> pd.DataFrame:
        week_array = ['Week' + str(x+1) for x in range(total_weeks)]
        df_columns = ['TeamId', 'TeamName']
        df_columns.extend(week_array)
        matchup_df = pd.DataFrame(data=matchup_array, columns=df_columns)
        matchup_df = matchup_df.astype({'TeamId': 'int32'})
        return matchup_df

    def get_team_count(self):
        return self.league_info.shape[0]

    def load_saved_weekly_results(self):
        loaded_df = self.local_data_manager.load_local_team_weekly_scores(self.league_id)

    def load_all_week_results(self, week):
        for index, fantasy_player in self.league_info.iterrows():
            team_id = fantasy_player[DATACONTRACT.TEAM_ID]
            team_name = fantasy_player[DATACONTRACT.TEAM_NAME]
            print(f'{team_id}/{team_name}')
            soup = self.web_helper.get_team_soup_by_week(self.league_id, team_id, week)
            self.team_parser.get_all_player_stats()

    def export_team_scores_df(self):
        self.scores_df.sort_values('TeamId').to_csv(f'{self.league_id}_Scores_{current_week}weeks.csv')

    def load_all_team_scores_to_date(self):
        for week in range(current_week):
            self.load_team_scores_by_week(week+1)

    def load_team_scores_through_week(self, week):
        for w in range(week):
            self.load_team_scores_by_week(w+1)

    def load_team_scores_by_week(self, week):
        score_array = []
        for index, fantasy_player in self.league_info.iterrows():
            team_id = fantasy_player[DATACONTRACT.TEAM_ID]
            team_name = fantasy_player[DATACONTRACT.TEAM_NAME]
            print(f'{team_id}/{team_name}')
            soup = self.web_helper.get_team_soup_by_week(self.league_id, team_id, week)
            real_score = self.team_parser.get_team_score(soup)
            proj_score = self.team_parser.get_team_projected_score(soup)
            # score_array.append([int(team_id), team_name, score])
            unique_id = f'{self.league_id}_{team_id}'
            score_array.append([unique_id, int(team_id), int(week), float(real_score), float(proj_score)])
        # if self.scores_df is None:
        #     # self.gen_scores_df_wide(score_array, week)
        #     self.gen_scores_df()
        #
        # else:
        #     self.append_scores_df_wide(score_array, week)
        self.append_scores_df(score_array)
        # print(score_array)
        # return score_array

    def gen_scores_df_wide(self, init_array, week):
        cols = ['TeamId', 'TeamName', f'Week_{week}_score']
        self.scores_df = pd.DataFrame(data=init_array, columns=cols)

    def gen_scores_df(self):
        cols = ['TeamId', 'TeamName', 'Week', 'Score']
        self.scores_df = pd.DataFrame(columns=cols)

    def append_scores_df(self, arr):
        # cols = ['TeamId', 'TeamName', 'Week', 'Score']
        # TEAMSCORECOLS = ['UniqueID', 'TeamId', 'Week', 'RealScore', 'ProjScore']
        temp_df = pd.DataFrame(data=arr, columns=DATACONTRACT.TEAMSCORECOLS)
        # print(temp_df)
        if self.scores_df is None:
            self.scores_df = temp_df
        else:
            self.scores_df = self.scores_df.append(temp_df)

    def append_scores_df_wide(self, scores_array, week):
        temp_df = pd.DataFrame(data = scores_array, columns=['TeamId', 'TeamName', 'Scores'])
        self.scores_df[f'Week_{week}_score'] = temp_df['Scores']

    def gen_player_stats_df(self):
        pass

    def load_data_point(self, week, time):
        for index, fantasy_player in self.league_info.iterrows():
            print(str(fantasy_player[DATACONTRACT.TEAM_ID]) + r'/' + fantasy_player[str(DATACONTRACT.TEAM_NAME)])
            team_id = fantasy_player[DATACONTRACT.TEAM_ID]
            team = Team.Team(self.league_id, team_id)
            team.load_soup_for_week(week, 0)
            team_data = team.parse_team_info()
            unique_id = str(self.league_id) + '_' + str(team_id)
            self.pandas_manager.add_team_info(team_data, [unique_id, week, time])
            team_player_data = team.parse_all_player_info()
            self.pandas_manager.add_player_info(team_player_data, [unique_id, week, time])

    def load_all_data_points(self, current_week):
        for week in range(current_week):
            print('Parsing week ' + str(current_week+1))
            self.load_data_point(week+1, 0)

    def save_league_data(self):
        teamfilename = str(self.league_id) + '_TeamData'
        self.local_data_manager.export_team_data(teamfilename)
        playerfilename = str(self.league_id) + '_PlayerData'
        self.local_data_manager.export_player_data(playerfilename)
