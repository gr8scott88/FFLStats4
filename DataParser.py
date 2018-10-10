import Helper as help


class DataParser:
    def __init__(self):
        pass

    def parse_team_stats(self, soup):
        team_score = float(self.get_team_score(soup))
        proj_score = float(self.get_team_projected_score(soup))
        return [team_score, proj_score]

    def parse_player_stats(self, soup):
        player_stats = self.get_player_info(soup)
        return player_stats

    def get_player_info(self, soup):
        # print('Parsing offensive players')
        all_player_info = []

        offensive_player_table = soup.find_all('table', id='statTable0')
        offensive_players = offensive_player_table[0].find('tbody').find_all('tr')

        for index, player in enumerate(offensive_players):
            # print('Parsing player: ' + str(index))
            all_player_info.append(help.floatify(self.parse_offensive_player(player)))

        # print('Parsing kicker')
        kicker_table = soup.find_all('table', id='statTable1')
        all_player_info.append(help.floatify(self.parse_kicker(kicker_table[0])))

        # print('Parsing defense')
        defensive_table = soup.find_all('table', id='statTable2')
        all_player_info.append(help.floatify(self.parse_defense(defensive_table[0])))

        return all_player_info

    @staticmethod
    def get_offensive_player_soup(soup, number):
        offensive_player_table = soup.find_all('table', id='statTable0')
        offensive_players = offensive_player_table[0].find('tbody').find_all('tr')
        return offensive_players[number]

    @staticmethod
    def get_defensive_player_soup(soup):
        defensive_table = soup.find_all('table', id='statTable2')
        return defensive_table[0]

    @staticmethod
    def get_kicker_player_soup(soup):
        kicker_table = soup.find_all('table', id='statTable1')
        return kicker_table[0]

    @staticmethod
    def get_team_score(soup):
        realscoreblock = soup.find_all('div', class_='Grid-table W-100 Fz-xs Py-lg')
        realscoreline = realscoreblock[0].find_all('p', class_="Inlineblock")
        realscorefield = realscoreline[0].contents[0]
        realscore = realscorefield.split(':')[1].split('pts')[0]
        return realscore

    @staticmethod
    def get_team_projected_score(soup):
        projhtml = soup.find_all(class_="Grid-table W-100 Fz-xs Py-lg")
        projspans = projhtml[0].find_all('span')
        projscore = projspans[1].contents[0]
        return projscore

    def parse_offensive_player(self, row_soup):
        data_indices = [0, 1, 5, 6, 7]
        if self.does_contain_forecast(row_soup):
            print('Has Forecast')
            data_indices = [0, 1, 6, 7, 8]

        data_soup = row_soup.find_all('td')
        active_position = data_soup[0].contents[0].find_all('span')[0].contents[0]
        player_name = data_soup[1].find_all('a', class_='Nowrap name F-link')[0].contents[0]
        player_position = data_soup[1].find_all('span', class_='Fz-xxs')[0].contents[0].split('-')[1].strip()
        if self.is_player_on_bye(data_soup):
            return_data = [player_name, player_position, active_position, 0, 0, 0]
        else:
            # print(data_soup)
            score = data_soup[data_indices[2]].contents[0].contents[0].contents[0]
            projected_score = data_soup[data_indices[3]].contents[0].contents[0]
            percent_start = data_soup[data_indices[4]].contents[0].contents[0].strip('%')
            # ['League', 'Team', 'Week', 'Time', 'Name', 'PlayerPos', 'ActivePos',
            # 'RealScore', 'ProjScore', 'PctPlayed']

            return_data = [player_name, player_position, active_position, score, projected_score, percent_start]
            # print(return_data)
        return return_data

    def parse_kicker(self, row_soup):
        data_indices = [0, 1, 5, 6, 7]
        if self.does_contain_forecast(row_soup):
            print('Has Forecast')
            data_indices = [0, 1, 5, 6, 7]

        data_soup = row_soup.find_all('td')
        # position = data_soup[0].contents[0].find_all('span')[0].contents[0]
        player_name = data_soup[1].find_all('a', class_='Nowrap name F-link')[0].contents[0]
        if self.is_player_on_bye(data_soup):
            print('Player: ' + player_name + ' is on Bye')
            return_data = [player_name, 'K', 'K', 0, 0, 0]
        else:
            score = data_soup[data_indices[2]].contents[0].contents[0].contents[0]
            projected_score = data_soup[data_indices[3]].contents[0].contents[0]
            percent_start = data_soup[data_indices[4]].contents[0].contents[0].strip('%')
            return_data = [player_name, 'K', 'K', score, projected_score, percent_start]
            # print(return_data)
        return return_data

    def parse_defense(self, row_soup):
        data_indices = [0, 1, 5, 6, 7]
        if self.does_contain_forecast(row_soup):
            # print('Has Forecast')
            data_indices = [0, 1, 5, 6, 7]

        data_soup = row_soup.find_all('td')
        # position = data_soup[0].contents[0].find_all('span')[0].contents[0]
        player_name = data_soup[1].find_all('a', class_='Nowrap name F-link')[0].contents[0]
        if self.is_player_on_bye(data_soup):
            return_data = [player_name, 'DEF', 'DEF', 0, 0, 0]
        else:
            score = data_soup[data_indices[2]].contents[0].contents[0].contents[0]
            projected_score = data_soup[data_indices[3]].contents[0].contents[0]
            percent_start = data_soup[data_indices[4]].contents[0].contents[0].strip('%')
            return_data = [player_name, 'DEF', 'DEF', score, projected_score, percent_start]
            # print(return_data)
        return return_data

    @staticmethod
    def is_player_on_bye(soup):
        if 'Bye' in str(soup):
            return True
        else:
            return False

    @staticmethod
    def does_contain_forecast(soup):
        array_length = len(soup)
        return array_length == 23
        # return str(soup).__contains__("Video Forecast")


