from bs4 import BeautifulSoup
import requests
from loguru import logger


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

    def build_draft_url(self, league_id, team_id):
        return self.build_url(league_id, team_id, 'draft')

    def build_matchup_url_by_week(self, league_id, team_id, week):
        html_league_and_team = self.build_url(league_id, team_id)
        return html_league_and_team + r'/matchup?&week=' + str(week) + '&mid1=1'

    def get_league_soup(self, league_id):
        url = self.build_url_for_league(league_id)
        logger.debug(url)
        return self.get_soup(url)

    def get_team_soup_by_week(self, league_id, team_id, week):
        url = self.build_team_url_by_week(league_id, team_id, week)
        logger.debug(url)
        return self.get_soup(url)

    def get_matchup_soup_by_week(self, league_id, team_id, week):
        url = self.build_matchup_url_by_week(league_id, team_id, week)
        logger.debug(url)
        return self.get_soup(url)

    def get_draft_soup(self, league_id, team_id):
        url = self.build_draft_url(league_id, team_id)
        logger.debug(url)
        return self.get_soup(url)

    @staticmethod
    def get_soup(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
