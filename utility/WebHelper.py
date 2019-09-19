from bs4 import BeautifulSoup
import requests


def build_url(root, *paths):
    url = root
    for path in paths:
        if url.endswith('/'):
            url = url + str(path)
        else:
            url = url + r'/' + str(path)
    return url


def build_url_for_week(root, league_id, team_id, week):
    html_league_and_team = build_url(root, league_id, team_id)
    return html_league_and_team + r'/team?&week=' + str(week)

# https://football.fantasysports.yahoo.com/f1/910981/4/team?&week=6


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup