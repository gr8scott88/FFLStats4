
# PLAYERSCORECOLS = [UNIQUE_ID, WEEK, 'Name',
#                    'PlayerPos', 'ActivePos', REAL_SCORE, PROJ_SCORE, 'PctPlayed']


class PlayerParser:
    def __init__(self):
        pass

    def get_all_player_info(self, soup):
        stat_table = soup.find_all('section', {'class': 'stat-target'})[0]
        sub_tables = stat_table.findChildren('div', recursive=False)
        offense_and_bench_table = sub_tables[0]
        kicker_table = sub_tables[1]
        defense_table = sub_tables[2]
        offense_and_bench_players = self.get_all_offensive_and_bench_players(offense_and_bench_table)
        defense_players = self.get_all_defense_info(defense_table)
        kicker_players = self.get_all_kicker_info(kicker_table)
        total_player_data = self.combine_all_data([offense_and_bench_players, defense_players, kicker_players])
        return total_player_data

    def get_table_rows(self, table_soup):
        return table_soup.find_all('tr')

    def get_table_colunms(self, row_soup):
        return row_soup.find_all('td')

    def is_player_row(self, row_soup):
        return 'href' in str(row_soup)

    def combine_all_data(self, arrays):
        out_array =[]
        for arr in arrays:
            out_array = out_array.extend(arr)
        return out_array

    def get_all_offensive_and_bench_players(self, offense_table):
        player_rows = self.get_table_rows(offense_table)
        all_data = []
        for row in player_rows:
            if self.is_player_row(row):
                new_data = self.parse_offensive_player(row)
                all_data.extend(new_data)
        return all_data

    def get_all_kicker_info(self, kicker_table):
        player_rows = self.get_table_rows(kicker_table)
        all_data = []
        for row in player_rows:
            if self.is_player_row(row):
                new_data = self.parse_kicker(row)
                all_data.extend(new_data)
        return all_data

    def get_all_defense_info(self, defense_table):
        player_rows = self.get_table_rows(defense_table)
        all_data = []
        for row in player_rows:
            if self.is_player_row(row):
                new_data = self.parse_defense(row)
                all_data.extend(new_data)
        return all_data

    def parse_offensive_player(self, soup):
        data_indices = [0, 1, 5, 6, 7]
        if self.does_contain_forecast(soup):
            # print('Has Forecast')
            data_indices = [0, 1, 6, 7, 8]

        data_soup = soup.find_all('td')
        active_position = data_soup[0].contents[0].find_all('span')[0].contents[0]

        if self.is_empty(soup):
            return_data = ['None', active_position, active_position, 0, 0, 0]
            return return_data
        else:
            player_position = data_soup[1].find_all('span', class_='Fz-xxs')[0].contents[0].split('-')[1].strip()

        player_name = data_soup[1].find_all('a', class_='Nowrap name F-link')[0].contents[0]

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

    def parse_kicker(self, soup):
        data_indices = [0, 1, 5, 6, 7]
        if self.does_contain_forecast(soup):
            # print('Has Forecast')
            data_indices = [0, 1, 5, 6, 7]

        data_soup = soup.find_all('td')
        # position = data_soup[0].contents[0].find_all('span')[0].contents[0]
        player_name = data_soup[1].find_all('a', class_='Nowrap name F-link')[0].contents[0]
        if self.is_player_on_bye(data_soup):
            # print('Player: ' + player_name + ' is on Bye')
            return_data = [player_name, 'K', 'K', 0, 0, 0]
        else:
            score = data_soup[data_indices[2]].contents[0].contents[0].contents[0]
            projected_score = data_soup[data_indices[3]].contents[0].contents[0]
            percent_start = data_soup[data_indices[4]].contents[0].contents[0].strip('%')
            return_data = [player_name, 'K', 'K', score, projected_score, percent_start]
            # print(return_data)
        return return_data

    def parse_defense(self, soup):
        data_indices = [0, 1, 5, 6, 7]
        if self.does_contain_forecast(soup):
            # print('Has Forecast')
            data_indices = [0, 1, 5, 6, 7]

        data_soup = soup.find_all('td')
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

    @staticmethod
    def is_empty(soup):
        return '(Empty)' in str(soup)