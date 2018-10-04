




def gen_url_panda(row, week_id):
    league_id = row['LeagueId']
    team_id = row['TeamId']
    parse_url = 'https://football.fantasysports.yahoo.com/f1/' + str(league_id) + '/' + str(
        team_id) + '/' + 'team?&week=' + str(week_id)
    print(parse_url)
    return parse_url


def gen_url_single(league_id, team_id, week_id):
    parse_url = 'https://football.fantasysports.yahoo.com/f1/' + str(league_id) + '/' + str(
        team_id) + '/' + 'team?&week=' + str(week_id)
    print(parse_url)
    return parse_url


def get_soup_single(league_id, team_id, week_id):
    url = gen_url_single(league_id, team_id, week_id)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def load_soup_single(file_path):
    with open(file_path, 'rb') as html:
        soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_all_info(team_info, week_id):
    for index, row in team_info.iterrows():
        # print(row['Team'], row['TeamId'], row['LeagueId'])
        parse_url = gen_url_panda(row, week_id)
        print(parse_url)
        soup = get_soup(parse_url)
        team_info = get_team_info(soup)
        all_player_info = get_player_info(soup)


def load_url(url):
    with open(url, 'rb') as html:
        soup = BeautifulSoup(html, 'html.parser')
        return soup











'''

save_file = r'C:\Dev\Python\FFLStats4\data\week3_910981_9.html'

with open(save_file) as f:
    soup = BeautifulSoup(f.read())
    # print(soup)

'''


'''

offensive_player_table = soup.find_all('table', id='statTable0')
offensive_players = offensive_player_table[0].find('tbody').find_all('tr')
offense0 = offensive_players[0]
tm.parse_offensive_player(offense0)

kicker_table = soup.find_all('table', id='statTable1')
kicker0 = kicker_table[0]
tm.parse_kicker(kicker0)

defensive_table = soup.find_all('table', id='statTable2')
defense0 = defensive_table[0]
tm.parse_defense(defense0)


'''


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




        team_columns = ['League', 'Team', 'Week', 'Time', 'RealScore', 'ProjScore']
        team_frame = pd.DataFrame(columns=team_columns)

        player_columns = ['League', 'Team', 'Week', 'Time', 'ActivePos', 'RealScore', 'ProjScore', 'PctPlayed']
        player_frame = pd.DataFrame(columns=player_columns)
