from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import os

# loaded_team_info = pd.read_csv('FFL_Info.csv')
# url = r"week3test.html"


def get_soup_single(league_id, team_id, week_id):
    url = gen_url_single(league_id, team_id, week_id)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def load_soup_single(file_path):
    with open(file_path, 'rb') as html:
        soup = BeautifulSoup(html)
    return soup


def load_url(url):
    with open(url, 'rb') as html:
        soup = BeautifulSoup(html)
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
    player_table = soup.find_all('table', id='statTable0')
    first_player = player_table[0].find_all('tr', class_='First')
    all_player_info.append(parse_player_row(first_player))

    other_players = player_table[0].find_all('tr', class_='Alt')

    for player in other_players:
        all_player_info.append(parse_player_row(player))

    bench_players = player_table[0].find_all('tr', class_='bench')

    for player in bench_players:
        all_player_info.append(parse_player_row(player))

    special_players = player_table[0].find_all('tr', class_='First Last')

    for player in special_players:
        all_player_info.append(parse_player_row(player))

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


def parse_player_row(row_soup):
    data_soup = row_soup.find_all('td')
    pos = data_soup[0].contents[0].find_all('span')[0].contents[0]
    score = data_soup[4].contents[0].contents[0].contents[0]
    proj = data_soup[5].contents[0].contents[0]
    return [pos, score, proj]


# get_all_info(team_info)


league = '910981'
team = '4'
week = '3'
# loaded_soup = get_soup_single(league, team, week)

loaded_soup = load_soup_single('week3test.html')
loaded_score = get_score(loaded_soup)
loaded_proj = get_projected(loaded_soup)


player_table = loaded_soup.find_all('table', id='statTable0')
first_player = player_table[0].find_all('tr', class_='First')
first_player = first_player[1]

parse_player_row(first_player)


parse_player_row(first_player)

other_players = player_table[0].find_all('tr', class_='Alt')

bench_players = player_table[0].find_all('tr', class_='bench')

special_players = player_table[0].find_all('tr', class_='First Last')

