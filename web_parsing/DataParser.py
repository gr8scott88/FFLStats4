from web_parsing import LeagueParser as lp, PlayerParser as pp, TeamParser as tp


class DataParser:
    def __init__(self):
        self.league = lp.LeagueParser()
        self.team = tp.TeamParser()
        self.player = pp.PlayerParser()
