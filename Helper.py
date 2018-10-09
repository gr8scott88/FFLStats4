from bs4 import BeautifulSoup
import requests


class UniqueID:
    def __init__(self, league_id, league_name, team_id, team_name, week_id, time_id=0):
        self.league_id = league_id
        self.team_id = team_id
        self.week = week_id
        self.time = time_id
        self.team_name = team_name
        self.league_name = league_name

    def get_id_array(self):
        return [self.league_id, self.league_name, self.team_id, self.team_name, self.week, self.time]

    def get_id_string(self):
        return 'ID: ' + 'Week ' + str(self.week) + ' Time ' + str(self.time) + ', ' + str(self.league_id) + ", " + str(self.team_id)


def get_soup_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_soup_file(html_file):
    with open(html_file) as current_html:
        soup = BeautifulSoup(current_html, 'html.parser')
    return soup


def floatify(array):
    for index in range(len(array)):
        try:
            array[index] = float(array[index])
        except Exception as e:
            # print(e)
            pass
    return array


