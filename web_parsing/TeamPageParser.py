from utility.YahooWebHelper import YahooWebHelper


class TeamParser:
    def __init__(self):
        pass

    def parse_team_stats(self, soup):
        team_score = float(self.get_team_score(soup))
        proj_score = float(self.get_team_projected_score(soup))
        return [team_score, proj_score]

    @staticmethod
    def get_team_projected_score(soup):
        projhtml = soup.find_all(class_="Grid-table W-100 Fz-xs Py-lg")
        projspans = projhtml[0].find_all('span')
        projscore = projspans[1].contents[0]
        return projscore

    def get_weekly_opponent(self, match_page_soup):
        matchup_box = match_page_soup.find_all('div', {'id': 'team-card-matchup'})[0]
        opponent = matchup_box.find_all('a', {'class': 'Grid-u'})[1]
        opponent_href = opponent.get('href')
        opponent_id = self.get_id_from_href(opponent_href)
        return opponent_id

    @staticmethod
    def get_id_from_href(href):
        arr = href.split('/')
        opponent_id = arr[-1]
        return opponent_id

    def get_team_roster(self):
        pass

    def get_all_player_stats(self, soup):
        stat_table = soup.find_all('section', {'class': 'stat-target'})[0]
        sub_tables = stat_table.findChildren('div', recursive=False)
        offense_and_bench = sub_tables[0]
        kickers = sub_tables[1]
        defense = sub_tables[2]

        pass

    def parse_offsense_stats(self, soup):
        pass

    def parse_kicker_stats(self, soup):
        pass

    def parse_defense_stats(self, soup):
        pass

    @staticmethod
    def get_team_score(soup):
        matchup_box = soup.find_all('div', {'id': 'team-card-matchup'})[0]
        current_player = matchup_box.find_all('div', {'class': 'Grid-u'})[0]
        current_player_score = current_player.get_text().strip('\n')
        return float(current_player_score)
