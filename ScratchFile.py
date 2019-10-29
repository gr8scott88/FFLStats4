from models import League
from utility.YahooWebHelper import YahooWebHelper
from web_parsing.MatchPageParser import MatchParser
from web_parsing.TeamPageParser import TeamParser
from data_handlers.PandasHandler import PandasDataHandler

helper = YahooWebHelper()
mp = MatchParser()
tp = TeamParser()
AFC_id = 609682
NFC_id = 713428

AFC = League.League(AFC_id)
NFC = League.League(NFC_id)

AFC.load_team_scores_through_week(7)
NFC.load_team_scores_through_week(7)

current_week = 2
for week in range(current_week):
    AFC.load_team_scores_by_week(week+1)

for week in range(current_week):
    NFC.load_team_scores_by_week(week+1)

# sdf = pd.DataFrame(data=scores)
# sorted_scores = sdf.sort_values('0')

s = helper.get_team_soup_by_week(AFC_id, 4, 4)
handler = PandasDataHandler()
