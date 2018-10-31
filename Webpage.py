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

    def save_team_html(self, week, time):
        file_path_info = self.parse_team_url()
        print(file_path_info)
        # file_path = os.path.join(file_path_info[0], file_path_info[2]
        league_dir = file_path_info[0]
        week_dir = 'week_' + str(week)
        file_path = os.path.join(league_dir, week_dir)
        file_name = str(file_path_info[1]) + '_' + str(time) + '.html'
        # print(file_path)
        # print(file_name)
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