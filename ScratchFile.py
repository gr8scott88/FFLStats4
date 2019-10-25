from models import League
from utility.YahooWebHelper import YahooWebHelper
from web_parsing.MatchPageParser import MatchParser
from web_parsing.TeamPageParser import TeamParser
import pandas as pd

helper = YahooWebHelper()
mp = MatchParser()
tp = TeamParser()
AFC_id = 609682
NFC_id = 713428

AFC = League.League(AFC_id)
NFC = League.League(NFC_id)

AFC.load_team_scores_through_week(2)


s = helper.get_team_soup_by_week(AFC_id, 1, 1)
p = tp.get_team_projected_score(s)
