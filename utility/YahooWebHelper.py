from bs4 import BeautifulSoup
import requests

# https://football.fantasysports.yahoo.com/f1/910981/4/team?&week=6


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

    def build_url_for_week(self, league_id, team_id, week):
        html_league_and_team = self.build_url(league_id, team_id)
        return html_league_and_team + r'/team?&week=' + str(week)

    @staticmethod
    def get_soup(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def get_league_soup(self, league_id):
        return self.get_soup(self.build_url_for_league(league_id))

    def get_week_soup(self, league_id, team_id, week):
        return self.build_url_for_week(league_id, team_id, week)
