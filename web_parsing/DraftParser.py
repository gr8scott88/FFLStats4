import pandas as pd
from models import DATACONTRACT
from loguru import logger


class DraftParser:
    def __init__(self):
        pass

    def parse_draft_info(self, draft_soup, info_dict):
        # DRAFTTRACKERCOLS = [UNIQUE_ID, LEAGUE_ID, TEAM_ID, TEAM_NAME, DRAFTORDER, CLASSORDER, PLAYERNAME, PLAYERPOS]
        team_table_section = draft_soup.find("section", {"id": "draft-team"})
        rows = team_table_section.find_all('tr')
        data_rows = rows[1::]
        all_data = []
        for row in data_rows:
            new_dict = {}
            new_dict.update(info_dict)
            row_dict = self.parse_draft_row(row)
            new_dict.update(row_dict)
            logger.debug(new_dict)
            all_data.append(new_dict)
        logger.debug(all_data)
        return pd.DataFrame(all_data)

    def parse_draft_row(self, row_soup) -> dict:
        tds = row_soup.find_all('td')
        draft_order = tds[0].contents[0]
        class_order = tds[1].contents[0].replace('(', '').replace(')', '')
        player_name = tds[2].find('a').contents[0]
        player_pos = tds[3].contents[0]
        row_dict = {DATACONTRACT.DRAFTORDER: draft_order,
                    DATACONTRACT.CLASSORDER: class_order,
                    DATACONTRACT.PLAYERNAME: player_name,
                    DATACONTRACT.PLAYERPOS: player_pos}
        logger.debug(row_dict)
        return row_dict




d1 = {DATACONTRACT.PLAYERPOS: 'WR', DATACONTRACT.PLAYERNAME: ['P1']}
d2 = {DATACONTRACT.PLAYERPOS: 'WR', DATACONTRACT.PLAYERNAME: ['P2']}
d3 = {DATACONTRACT.PLAYERPOS: ['QB'], DATACONTRACT.PLAYERNAME: ['P3']}
d4 = {DATACONTRACT.PLAYERPOS: ['QB'], DATACONTRACT.DRAFTORDER: ['5']}

l = [d1, d2, d3, d4]

df = pd.DataFrame(l)


df = pd.DataFrame.from_dict(d1)

df.append(pd.DataFrame.from_dict(d2))

d = {DATACONTRACT.PLAYERPOS: ['WR', 'WR', 'QB'], DATACONTRACT.PLAYERNAME: ['P1', 'P2', 'P3']}
df = pd.DataFrame.from_dict(d)


d1 = {'r1': 1, 'r2': 2}
d2 = {'r3': 3, 'r4': 4}