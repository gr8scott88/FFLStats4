from models import League
from utility.YahooWebHelper import YahooWebHelper
from web_parsing.MatchPageParser import MatchParser
from web_parsing.TeamPageParser import TeamParser

# helper = YahooWebHelper()
# mp = MatchParser()
# tp = TeamParser()

AFC_id = 609682
AFC = League.League(AFC_id)

NFC_id = 713428
NFC = League.League(NFC_id)

# opp = tp.get_weekly_opponent(helper.get_team_soup_by_week(AFC_id, 4, 6))
NFC.matchup_info.astype({'TeamId':'int32'}).reset_index().to_csv('nfc_matchup.csv')
NFC.matchup_info.astype({'TeamId':'int32'}).sort_values('TeamId').reset_index().to_csv('nfc_matchup.csv')

AFC.matchup_info.astype({'TeamId':'int32'}).sort_values('TeamId').reset_index().to_csv('afc_matchup.csv')