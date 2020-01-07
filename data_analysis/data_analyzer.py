from models.League import League

class DataAnalyser:
    def __init__(self, league: League):
        self.league_info = league.league_info
        self.draft_info = league.draft_info
        self.matchup_info = league.matchup_info
        self.score_info = league.score_info
        self.player_info = league.player_info

    def cum_score_top_x_draft_pics(self, x):
