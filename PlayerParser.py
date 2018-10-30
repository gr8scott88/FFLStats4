
class PlayerParser:
    def __init__(self):
        pass

    def parse_offensive_player(self, soup):
        data_indices = [0, 1, 5, 6, 7]
        if self.does_contain_forecast(soup):
            print('Has Forecast')
            data_indices = [0, 1, 6, 7, 8]

        data_soup = soup.find_all('td')
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

    def parse_kicker(self, soup):
        data_indices = [0, 1, 5, 6, 7]
        if self.does_contain_forecast(soup):
            print('Has Forecast')
            data_indices = [0, 1, 5, 6, 7]

        data_soup = soup.find_all('td')
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
