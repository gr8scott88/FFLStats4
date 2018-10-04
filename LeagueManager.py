import TeamManager as tm
import Helper
import DataManager


class LeagueManager:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.team_manager = tm.TeamManager(data_manager)

    def load_league(self, week_id):
        league_info = self.data_manager.get_league_attributes()

        all_league_data = []

        for index, row in league_info.iterrows():
            team_id = row['TeamId']
            league_id = row['LeagueId']
            unique_id = Helper.UniqueID(league_id, team_id, week_id)
            print('Parsing team: ' + str(league_id) + r'/' + str(team_id))
            all_data_for_team = self.team_manager.get_team_info(unique_id)

            all_league_data.append(all_data_for_team)
            print(all_data_for_team)

        for team in all_league_data:
            team_row = team[0] + team[1]
            self.data_manager.add_team_from_row(team_row)
            player_array = team[2]
            for player in player_array:
                player_row = team[0] + player
                self.data_manager.add_player_from_row(player_row)
