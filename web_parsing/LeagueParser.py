import pandas as pd
from bs4 import BeautifulSoup
from models import DATACONTRACT
from utility.YahooWebHelper import YahooWebHelper


class LeagueParser:
    def __init__(self, league_id, web_helper: YahooWebHelper):
        self.web_helper = web_helper
        self.league_id = league_id

    def parse_league_info(self) -> pd.DataFrame:
        league_info = []
        league_soup = self.web_helper.get_league_soup(self.league_id)
        league_table = league_soup.find_all('ul', class_='List-rich')
        players = league_table[0].find_all('a', class_='F-link')
        for player in players:
            team_name = player.contents[0]
            href = player['href']
            info = self.parse_href(href)
            league_id = info[0]
            team_id = info[1]
            unique_id = str(league_id + '_' + str(team_id))
            league_info.append([unique_id, league_id, team_id, team_name])
        league_frame = pd.DataFrame(league_info, columns=[DATACONTRACT.LEAGUEINFOCOLS[0],
                                                          DATACONTRACT.LEAGUEINFOCOLS[1],
                                                          DATACONTRACT.LEAGUEINFOCOLS[2],
                                                          DATACONTRACT.LEAGUEINFOCOLS[3]])
        return league_frame

    @staticmethod
    def parse_href(href):
        info = href.split('/')
        league_id = info[2]
        team_id = info[3]
        return [league_id, team_id]
