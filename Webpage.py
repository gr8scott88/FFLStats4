import requests
from bs4 import BeautifulSoup
import FileManager
import os


class Webpage:
    def __init__(self, url: str):
        self.url = url
        page = requests.get(url)
        self.content = page.content
        self.soup = BeautifulSoup(self.content, 'html.parser')

    def save_team_html(self):
        file_path_info = self.parse_team_url()
        file_path = os.path.join(file_path_info[0], file_path_info[2])
        file_name = 'Team_' + str(file_path_info[1] + '.html')
        FileManager.save_html(file_path, file_name, self.content)

    def get_soup(self):
        return self.soup

    def parse_team_url(self):
        # https://football.fantasysports.yahoo.com/f1/910981/4/team?&week=5
        info = self.url.split('/')
        league = info[4]
        team = info[5]
        week = info[6]
        return [league, team, week]

    def parse_league_html(self):
        # https://football.fantasysports.yahoo.com/f1/910981
        info = self.url.split('/')
        league = info[4]
        return league

    def save_league_html(self):
        league = self.parse_league_html()
        file_name = 'LeagueHtml_' + str(league) + '.html'
        FileManager.save_html(league, file_name, self.content)