from bs4 import BeautifulSoup
import requests


class YahooWebHelper:
    def __init__(self):
        self.root = r'https://football.fantasysports.yahoo.com/f1'

    def build_url(self, *paths):
        url = self.root
        for path in paths:
            if url.endswith('/'):
                url = url + str(path)
            else:
                url = url + r'/' + str(path)
        return url

    def build_url_for_league(self, league_id):
        return f'{self.root}/{str(league_id)}'

    def build_team_url_by_week(self, league_id, team_id, week):
        html_league_and_team = self.build_url(league_id, team_id)
        return html_league_and_team + r'/team?&week=' + str(week)

    def build_matchup_url_by_week(self, league_id, team_id, week):
        html_league_and_team = self.build_url(league_id, team_id)
        return html_league_and_team + r'/matchup?&week=' + str(week)

    def get_league_soup(self, league_id):
        return self.get_soup(self.build_url_for_league(league_id))

    def get_team_soup_by_week(self, league_id, team_id, week):
        return self.get_soup(self.build_team_url_by_week(league_id, team_id, week))

    def get_matchup_soup_by_week(self, league_id, team_id, week):
        return self.get_soup(self.build_matchup_url_by_week(league_id, team_id, week))

    @staticmethod
    def get_soup(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
