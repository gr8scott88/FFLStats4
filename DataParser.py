import LeagueParser as lp
import TeamParser as tp
import PlayerParser as pp


class DataParser:
    def __init__(self):
        self.league = lp.LeagueParser()
        self.team = tp.TeamParser()
        self.player = pp.PlayerParser()
