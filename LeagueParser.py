import pandas as pd
from bs4 import BeautifulSoup
import DATACONTRACT


class LeagueParser:
    def __init__(self):
        pass

    def parse_league_info(self, league_soup: BeautifulSoup):
        league_info = []
        league_table = league_soup.find_all('ul', class_='List-rich')
        players = league_table[0].find_all('a', class_='F-link')
        for player in players:
            team_name = player.contents[0]
            href = player['href']
            info = self.parse_href(href)
            league_id = info[0]
            team_id = info[1]
            league_info.append([league_id, team_id, team_name])
        league_frame = pd.DataFrame(league_info, columns=[DATACONTRACT.LEAGUECOLS[0], DATACONTRACT.LEAGUECOLS[1],
                                                          DATACONTRACT.LEAGUECOLS[2]])
        return league_frame

    @staticmethod
    def parse_href(href):
        info = href.split('/')
        league_id = info[2]
        team_id = info[3]
        return [league_id, team_id]
