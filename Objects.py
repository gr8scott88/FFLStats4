class UniqueID:
    def __init__(self, league_id, team_id, week_id, time_id=0):
        self.league = league_id
        self.team = team_id
        self.week = week_id
        self.time = time_id

    def get_id_array(self):
        return [self.league, self.team, self.week, self.time]

    def get_id_string(self):
        return 'ID: ' + 'Week ' + str(self.week) + ' Time ' + str(self.time) + ', ' + str(self.league) + ", " + str(self.team)