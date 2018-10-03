from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import os
import unicodedata

local_path = r'C:\Dev\Python\FFLStats4'


def get_team_info(league_id, team_id, week_id):
    soup = get_soup(league_id, team_id, week_id)
    all_data = parse_all_stats(soup)
    return all_data


def get_soup(league_id, team_id, week_id):
    save_file = gen_save_file(league_id, team_id, week_id)
    script_path = ''
    try:
        script_path = os.path.dirname(os.path.realpath(__file__))
    except Exception as e:
        script_path = local_path

    relative_path = 'data\\' + save_file

    file_path = os.path.join(script_path, relative_path)
    print(file_path)

    if os.path.isfile(file_path):
        print('Loading file: ' + file_path)
        soup = load_html(file_path)
    else:
        url = gen_url(league_id, team_id, week_id)
        print('Downloading web page: ' + url)
        soup = download_html(url, file_path)\

    # print(soup)
    return soup


def gen_save_file(league_id, team_id, week_id):
    save_name = 'week' + str(week_id) + '_' + str(league_id) + '_' + str(team_id) + '.html'
    return save_name


def download_html(url, fpath):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    with open(fpath, 'wb') as f:
        # f.write(soup.encode('utf-8'))
        f.write(str(page.content).encode('utf-8'))

    return soup


def load_html(save_file):
    with open(save_file) as f:
        soup = BeautifulSoup(f.read())
        # print(soup)
    return soup


def gen_url(league_id, team_id, week_id):
    parse_url = 'https://football.fantasysports.yahoo.com/f1/' + str(league_id) + '/' + str(
    team_id) + '/' + 'team?&week=' + str(week_id)
    return parse_url


def parse_all_stats(soup):
    team_stats = parse_team_stats(soup)
    player_stats = parse_player_stats(soup)
    return [team_stats, player_stats]


def parse_team_stats(soup):
    team_score = get_team_score(soup)
    proj_score = get_team_projected_score(soup)
    return [team_score, proj_score]


def parse_player_stats(soup):
    player_stats = get_player_info(soup)
    return player_stats


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


def get_team_score(soup):
    realscoreblock = soup.find_all('div', class_='Grid-table W-100 Fz-xs Py-lg')
    realscoreline = realscoreblock[0].find_all('p', class_="Inlineblock")
    realscorefield = realscoreline[0].contents[0]
    realscore = realscorefield.split(':')[1].split('pts')[0]
    return realscore


def get_team_projected_score(soup):
    projhtml = soup.find_all(class_="Grid-table W-100 Fz-xs Py-lg")
    projspans = projhtml[0].find_all('span')
    projscore = projspans[1].contents[0]
    return projscore


def parse_offensive_player(row_soup):
    data_soup = row_soup.find_all('td')
    position = data_soup[0].contents[0].find_all('span')[0].contents[0]
    score = data_soup[6].contents[0].contents[0].contents[0]
    projected_score = data_soup[7].contents[0].contents[0]
    percent_start = data_soup[8].contents[0].contents[0].strip('%')
    return_data = [position, score, projected_score, percent_start]
    # print(return_data)
    return return_data


def parse_kicker(row_soup):
    data_soup = row_soup.find_all('td')
    position = data_soup[0].contents[0].find_all('span')[0].contents[0]
    score = data_soup[5].contents[0].contents[0].contents[0]
    projected_score = data_soup[6].contents[0].contents[0]
    percent_start = data_soup[7].contents[0].contents[0].strip('%')
    return_data = [position, score, projected_score, percent_start]
    # print(return_data)
    return return_data


def parse_defense(row_soup):
    data_soup = row_soup.find_all('td')
    position = data_soup[0].contents[0].find_all('span')[0].contents[0]
    score = data_soup[5].contents[0].contents[0].contents[0]
    projected_score = data_soup[6].contents[0].contents[0]
    percent_start = data_soup[7].contents[0].contents[0].strip('%')
    return_data = [position, score, projected_score, percent_start]
    # print(return_data)
    return return_data











def gen_save_html_panda(row, week_id):
    league_id = row['LeagueId']
    team_id = row['TeamId']
    save_name = 'week' + week_id + '_' + league_id + '_' + team_id + '.html'
    return save_name


def save_player_info(data_array):
    print(data_array)
    pass


def save_team_info(data_array):
    pass












