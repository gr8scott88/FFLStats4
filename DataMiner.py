from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import os

week = 2
team_info = pd.read_csv('FFL_Info.csv')
url = r"week3test.html"


def load_url(url):
    with open(url, 'rb') as html:
        soup = BeautifulSoup(html)
        return soup


def get_all_info(team_info):
    for index, row in team_info.iterrows():
        # print(row['Team'], row['TeamId'], row['LeagueId'])
        gen_url(row)


def get_score(soup):
    realscoreblock = soup.find_all('div', class_='Grid-table W-100 Fz-xs Py-lg')
    realscoreline = realscoreblock[0].find_all('p', class_="Inlineblock")
    realscorefield = realscoreline[0].contents[0]
    realscore = realscorefield.split(':')[1].split('pts')[0]
    return realscore


def get_projected(soup):
    projhtml = soup.find_all(class_="Grid-table W-100 Fz-xs Py-lg")
    projspans = projhtml[0].find_all('span')
    projscore = projspans[1].contents[0]
    return projscore


def get_score_table(soup):
    pass


def get_score_line(score_table):
    pass


def get_info(score_line):
    pass


def get_html(row):
    save_file = gen_save_html(row)
    fpath = '\\data\\' + save_file
    os.path.isfile(fpath)
    pass


def download_html(url, savename):
    page = requests.get(url)
    pass


def load_html(url):
    pass


def gen_url(row):
    league = row['LeagueId']
    team = row['TeamId']
    parse_url = 'https://football.fantasysports.yahoo.com/f1/' + str(league) + '/' + str(team) + '/' + 'team?&week=' + str(week)
    print(parse_url)
    return parse_url


def gen_save_html(row):
    league = row['LeagueId']
    team = row['TeamId']
    save_name = 'week' + week + '_' + league + '_' + team + '.html'
    return save_name


get_all_info(team_info)