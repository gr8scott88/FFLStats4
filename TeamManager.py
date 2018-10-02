from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import os


def get_soup_single(league_id, team_id, week_id):
    url = gen_url_single(league_id, team_id, week_id)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def load_soup_single(file_path):
    with open(file_path, 'rb') as html:
        soup = BeautifulSoup(html, 'html.parser')
    return soup


def load_url(url):
    with open(url, 'rb') as html:
        soup = BeautifulSoup(html, 'html.parser')
        return soup


def get_all_info(team_info, week_id):
    for index, row in team_info.iterrows():
        # print(row['Team'], row['TeamId'], row['LeagueId'])
        parse_url = gen_url(row, week_id)
        print(parse_url)
        soup = get_soup(parse_url)
        team_info = get_team_info(soup)
        all_player_info = get_player_info(soup)


def get_team_info(soup):
    score = get_score(soup)
    proj_score = get_projected(soup)
    return [score, proj_score]


def get_player_info(soup):
    all_player_info = []

    offensive_player_table = soup.find_all('table', id='statTable0')
    offensive_players = offensive_player_table[0].find('tbody').find_all('tr')

    for player in offensive_players:
        all_player_info.append(parse_offensive_player(player))

    kicker_table = soup.find_all('table', id='statTable1')
    all_player_info.append(parse_kicker(kicker_table[0]))

    defensive_table = soup.find_all('table', id='statTable2')
    all_player_info.append(parse_defense(defensive_table[0]))

    return all_player_info


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


def get_soup(team_id, url, week_id):
    save_file = gen_save_html(team_id, week_id)
    fpath = '\\data\\' + save_file
    if os.path.isfile(fpath):
        soup = load_html(save_file)
    else:
        soup = download_html(url, save_file)
    return soup


def download_html(url, savename):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def load_html(save_file):
    soup = BeautifulSoup(open(save_file).read())
    return soup


def gen_url(row, week_id):
    league_id = row['LeagueId']
    team_id = row['TeamId']
    parse_url = 'https://football.fantasysports.yahoo.com/f1/' + str(league_id) + '/' + str(team_id) + '/' + 'team?&week=' + str(week_id)
    print(parse_url)
    return parse_url


def gen_url_single(league_id, team_id, week_id):
    parse_url = 'https://football.fantasysports.yahoo.com/f1/' + str(league_id) + '/' + str(team_id) + '/' + 'team?&week=' + str(week_id)
    print(parse_url)
    return parse_url


def gen_save_html(row, week_id):
    league_id = row['LeagueId']
    team_id = row['TeamId']
    save_name = 'week' + week_id + '_' + league_id + '_' + team_id + '.html'
    return save_name


def save_player_info(data_array):
    print(data_array)
    pass


def save_team_info(data_array):
    pass


def parse_offensive_player(row_soup):
    data_soup = row_soup.find_all('td')
    position = data_soup[0].contents[0].find_all('span')[0].contents[0]
    score = data_soup[4].contents[0].contents[0].contents[0]
    projected_score = data_soup[5].contents[0].contents[0]
    percent_start = data_soup[6].contents[0].contents[0].strip('%')
    return [position, score, projected_score, percent_start]


def parse_kicker(row_soup):
    data_soup = row_soup.find_all('td')
    position = data_soup[0].contents[0].find_all('span')[0].contents[0]
    score = data_soup[3].contents[0].contents[0].contents[0]
    projected_score = data_soup[4].contents[0].contents[0]
    percent_start = data_soup[5].contents[0].contents[0].strip('%')
    return [position, score, projected_score, percent_start]


def parse_defense(row_soup):
    data_soup = row_soup.find_all('td')
    position = data_soup[0].contents[0].find_all('span')[0].contents[0]
    score = data_soup[3].contents[0].contents[0].contents[0]
    projected_score = data_soup[4].contents[0].contents[0]
    percent_start = data_soup[5].contents[0].contents[0].strip('%')
    return [position, score, projected_score, percent_start]


def get_team_info(team_id, league_id, week):


