import pandas as pd
from models import Team, DATACONTRACT
from web_parsing.LeaguePageParser import LeaguePageParser
from web_parsing.MatchPageParser import MatchParser
from web_parsing.TeamPageParser import TeamParser
from web_parsing.PlayerParser import PlayerParser
from web_parsing.DraftParser import DraftParser
import data_storage.LocalDataManager as dm
from data_handlers.PandasHandler import PandasDataHandler
from utility.YahooWebHelper import YahooWebHelper
from loguru import logger

total_weeks = 16
current_week = 7


class League:
    def __init__(self, league_id, name_):
        self.league_id = league_id
        self.name = name_
        self.league_parser = LeaguePageParser()
        self.match_parser = MatchParser()
        self.draft_parser = DraftParser()
        self.team_parser = TeamParser()
        self.player_parser = PlayerParser()
        self.web_helper = YahooWebHelper()
        self.pandas_manager = PandasDataHandler()
        self.league_info = self.load_league_info()
        self.draft_info = self.load_draft_info()
        self.matchup_info = self.load_matchup_info()
        self.score_info = self.load_score_info()
        self.player_info = self.load_player_info()
        # self.rank_info = self.calculate_rank()

    def reload_player_info(self):
        self.player_info = self.load_player_info()

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

    def load_draft_info(self) -> pd.DataFrame:
        draft_df = dm.load_from_parquet(self.league_id, DATACONTRACT.DRAFTFILENAME)
        if draft_df is None:
            for index, team_row in self.league_info.iterrows():
                team_id = team_row[DATACONTRACT.TEAM_ID]
                team_name = team_row[DATACONTRACT.TEAM_NAME]
                unique_id = f'{self.league_id}_{team_id}'
                # [UNIQUE_ID, LEAGUE_ID, TEAM_ID, TEAM_NAME,
                info_dict = {DATACONTRACT.UNIQUE_ID: unique_id,
                             DATACONTRACT.LEAGUE_ID: self.league_id,
                             DATACONTRACT.TEAM_ID: team_id,
                             DATACONTRACT.TEAM_NAME: team_name}
                draft_soup = self.web_helper.get_draft_soup(self.league_id, team_id)
                if draft_df is None:
                    draft_df = self.draft_parser.parse_draft_info(draft_soup, info_dict)
                else:
                    draft_df = draft_df.append(self.draft_parser.parse_draft_info(draft_soup, info_dict))

            dm.save_to_parquet(self.league_id, draft_df, DATACONTRACT.DRAFTFILENAME, False)
            print('Loaded Draft Info from WEB')
        else:
            print('Loaded Draft Info from PARQUET file')
        return draft_df

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

    def load_player_info(self):
        return dm.load_from_parquet(self.league_id, DATACONTRACT.PLAYERFILENAME)

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

    def is_week_player_data_loaded(self, week):
        # logger.debug(f'Loading player scores for week {week}')
        if self.player_info is None:
            # logger.debug('Player info doesn\'t exist')
            return False
        else:
            res = week in self.player_info['Week'].to_list()
            # logger.debug(f'Looking in week {week} result is {res}')
            return res

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

    def load_all_player_data_through_week(self, week):
        for w in range(week):
            self.load_player_data_by_week(w + 1, save_data=True)

    def load_player_data_by_week(self, week, save_data=False):
        if not self.is_week_player_data_loaded(week):
            for index, fantasy_player in self.league_info.iterrows():
                team_id = fantasy_player[DATACONTRACT.TEAM_ID]
                team_name = fantasy_player[DATACONTRACT.TEAM_NAME]
                print(f'{team_id}/{team_name}')
                soup = self.web_helper.get_team_soup_by_week(self.league_id, team_id, week)
                player_array = self.player_parser.get_all_info(soup)
                unique_id = f'{self.league_id}_{team_id}'
                # PLAYERSCORECOLS = [UNIQUE_ID, WEEK, 'Name',
                #                    'PlayerPos', 'ActivePos', REAL_SCORE, PROJ_SCORE, 'PctPlayed']

                player_df = pd.DataFrame(columns=DATACONTRACT.PLAYERPARSECOLS, data=player_array)
                player_df[DATACONTRACT.UNIQUE_ID] = unique_id
                player_df[DATACONTRACT.WEEK] = week
                # player_array.append([unique_id, int(team_id), int(week), float(real_score), float(proj_score)])
                # matchup_df = matchup_df.astype({'TeamId': 'int32'})
                player_df = player_df.astype({f'{DATACONTRACT.REAL_SCORE}': 'float'})
                player_df = player_df.astype({f'{DATACONTRACT.PROJ_SCORE}': 'float'})
                player_df = player_df.astype({f'{DATACONTRACT.PCTSTART}': 'float'})
                player_df = player_df.astype({f'{DATACONTRACT.WEEK}': 'int'})
                self.append_player_stats_df(player_df)
            if save_data:
                dm.save_to_parquet(self.league_id, self.player_info, DATACONTRACT.PLAYERFILENAME, True)

    def append_player_stats_df(self, df):
        # PLAYERSCORECOLS = [UNIQUE_ID, WEEK, 'Name',
        #                    'PlayerPos', 'ActivePos', REAL_SCORE, PROJ_SCORE, 'PctPlayed']
        # temp_df = pd.DataFrame(data=arr, columns=DATACONTRACT.TEAMSCORECOLS)
        # print(temp_df)
        if self.player_info is None:
            self.player_info = df
        else:
            self.player_info = self.player_info.append(df)

    def calculate_rank(self):
        loaded_weeks = self.score_info['Week'].max()
        self.gen_ranking_df()
        for week in loaded_weeks:
            for index, fantasy_player in self.league_info.iterrows():
                #TODO
                pass

    def gen_ranking_df(self):
        # RANKINGTRACKERCOLS = [UNIQUE_ID, LEAGUE_ID, TEAM_ID, TEAM_NAME, WEEK, RESULT, TOTALWINS, TEAMRANKING]
        self.rank_info = pd.DataFrame(columns=DATACONTRACT.RANKINGTRACKERCOLS)


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
