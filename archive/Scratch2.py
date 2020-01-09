from web_parsing.DraftParser import DraftParser
from utility.YahooWebHelper import YahooWebHelper
from models import DATACONTRACT
helper = YahooWebHelper()


league_id = 609682
team_id = 1
unique_id = f'{league_id}_{team_id}'
s = helper.get_draft_soup(league_id, team_id)
dp = DraftParser()

# DRAFTTRACKERCOLS = [UNIQUE_ID, LEAGUE_ID, TEAM_ID, DRAFTORDER, CLASSORDER, PLAYERNAME, PLAYERPOS]
info_dict = {DATACONTRACT.UNIQUE_ID: unique_id,
             DATACONTRACT.LEAGUE_ID: league_id,
             DATACONTRACT.TEAM_ID: team_id}

test = dp.parse_draft_info(s, info_dict)

