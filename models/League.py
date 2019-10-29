import pandas as pd
from models import Team, DATACONTRACT
from web_parsing.LeaguePageParser import LeaguePageParser
from web_parsing.MatchPageParser import MatchParser
from web_parsing.TeamPageParser import TeamParser
import data_storage.LocalDataManager as dm
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
        self.pandas_manager = PandasDataHandler()
        self.league_info = self.load_league_info()
        self.matchup_info = self.load_matchup_info()
        self.score_info = self.load_score_info()

    def load_league_info(self) -> pd.DataFrame:
        league_df = dm.load_from_parquet(self.league_id, DATACONTRACT.LEAGUEFILENAME)
        if league_df is None:
            league_soup = self.web_helper.get_league_soup(self.league_id)
            league_df = self.league_parser.parse_league_info(league_soup)
            print('Loaded League Info from WEB')
            dm.save_to_parquet(self.league_id, league_df, DATACONTRACT.LEAGUEFILENAME, False)
        else:
            print('Loaded League Info from PARQUET file')
        return league_df

    def load_matchup_info(self) -> pd.DataFrame:
        matchup_df = dm.load_from_parquet(self.league_id, DATACONTRACT.MATCHUPFILENAME)
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
            dm.save_to_parquet(self.league_id, matchup_df, DATACONTRACT.MATCHUPFILENAME, False)
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

    def load_score_info(self):
        return dm.load_from_parquet(self.league_id, DATACONTRACT.SCOREFILENAME)

    def load_all_team_scores_to_date(self):
        for week in range(current_week):
            self.load_team_scores_by_week(week+1, save_data=True)

    def load_team_scores_through_week(self, week):
        for w in range(week):
            self.load_team_scores_by_week(w+1, save_data=True)

    def is_week_loaded(self, week):
        if self.score_info is None:
            return False
        else:
            return week in self.score_info['Week'].to_list()

    def load_team_scores_by_week(self, week, save_data=False):
        if not self.is_week_loaded(week):
            score_array = []
            for index, fantasy_player in self.league_info.iterrows():
                team_id = fantasy_player[DATACONTRACT.TEAM_ID]
                team_name = fantasy_player[DATACONTRACT.TEAM_NAME]
                print(f'{team_id}/{team_name}')
                soup = self.web_helper.get_team_soup_by_week(self.league_id, team_id, week)
                real_score = self.team_parser.get_team_score(soup)
                proj_score = self.team_parser.get_team_projected_score(soup)
                unique_id = f'{self.league_id}_{team_id}'
                # TEAMSCORECOLS = ['UniqueID', 'TeamId', 'Week', 'RealScore', 'ProjScore']
                score_array.append([unique_id, int(team_id), int(week), float(real_score), float(proj_score)])
            self.append_scores_df(score_array)
            if save_data:
                dm.save_to_parquet(self.league_id, self.score_info, DATACONTRACT.SCOREFILENAME, True)

    def append_scores_df(self, arr):
        # TEAMSCORECOLS = ['UniqueID', 'TeamId', 'Week', 'RealScore', 'ProjScore']
        temp_df = pd.DataFrame(data=arr, columns=DATACONTRACT.TEAMSCORECOLS)
        # print(temp_df)
        if self.score_info is None:
            self.score_info = temp_df
        else:
            self.score_info = self.score_info.append(temp_df)

    def gen_player_stats_df(self):
        pass

    def export_league_data_to_csv(self):
        leaguefilename = str(self.league_id) + 'LeagueData'
        dm.export_to_csv(self.league_info, leaguefilename)
        matchupfilename = str(self.league_id) + '_MatchupData'
        dm.export_to_csv(self.matchup_info, matchupfilename)
        scorefilename = str(leaguefilename) + '_ScoreData'
        dm.export_to_csv(self.score_info, scorefilename)

    def export_friendly_score_data(self):
        week_array = self.score_info['Week'].unique()
        for week in week_array:
            temp = self.score_info.loc[self.score_info['Week'] == week]
        pass

    def print_info(self):
        print(self.league_info)
        print(self.matchup_info)
        print(self.score_info)

    ##### BELOW IS SCRATCH #####

    def load_all_week_results(self, week):
        for index, fantasy_player in self.league_info.iterrows():
            team_id = fantasy_player[DATACONTRACT.TEAM_ID]
            team_name = fantasy_player[DATACONTRACT.TEAM_NAME]
            print(f'{team_id}/{team_name}')
            soup = self.web_helper.get_team_soup_by_week(self.league_id, team_id, week)
            self.team_parser.get_all_player_stats()

    def export_team_scores_df(self):
        self.score_info.sort_values('TeamId').to_csv(f'{self.league_id}_Scores_{current_week}weeks.csv')

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
