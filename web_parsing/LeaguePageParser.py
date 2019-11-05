import pandas as pd
from models import DATACONTRACT


class LeaguePageParser:
    def __init__(self):
        pass

    def parse_league_info(self, league_page_soup) -> pd.DataFrame:
        league_info = []
        players = self.get_player_table(league_page_soup)
        for player in players:
            team_name = player.contents[0]
            href = player['href']
            info = self.parse_href(href)
            league_id = info[0]
            team_id = info[1]
            unique_id = str(league_id + '_' + str(team_id))
            league_info.append([unique_id, league_id, int(team_id), team_name])
        league_frame = pd.DataFrame(league_info, columns=[DATACONTRACT.LEAGUEINFOCOLS[0],
                                                          DATACONTRACT.LEAGUEINFOCOLS[1],
                                                          DATACONTRACT.LEAGUEINFOCOLS[2],
                                                          DATACONTRACT.LEAGUEINFOCOLS[3]])
        return league_frame

    @staticmethod
    def get_player_table(league_page_soup):
        league_table = league_page_soup.find_all('ul', class_='List-rich')
        players = league_table[0].find_all('a', class_='F-link')
        return players

    @staticmethod
    def get_standings_table(league_page_soup):
        standings_table = league_page_soup.find("section", {"id": "leaguestandings"})
        return standings_table

    def get_standings_info(self):
        standings_table = self.get_standings_table()
        standings_rows = standings_table.find_all('tr')
        for row in standings_rows:
            standings_row_info = self.parse_standings_row(row)

    @staticmethod
    def parse_standings_row(standings_row):
        row_info = standings_row.find_all('td')
        href = standings_row[1].find_all('a')[1].get('href')
        team_id = href.split('/')[-1]
        rank = row_info[0].find_all('span')[1].contents[0]
        name = row_info[1].find_all('a')[1].contents[0]
        WLT = row_info[2].contents[0]
        PF = row_info[3].contents[0]
        PA = row_info[4].contents[0]
        Streak = row_info[5].contents[0]
        Waiver = row_info[6].contents[0]
        Moves = row_info[7].contents[0]
        return [team_id, rank, name, WLT, PF, PA, Streak, Waiver, Moves]

    def get_team_names(self):
        team_names = []
        players = self.get_player_table()
        for player in players:
            team_name = player.contents[0]
            team_names.append(team_name)
        return team_names

    def get_current_standings(self):
        pass

    @staticmethod
    def parse_href(href):
        info = href.split('/')
        league_id = info[2]
        team_id = info[3]
        return [league_id, team_id]
