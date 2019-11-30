from loguru import logger

# PLAYERSCORECOLS = [UNIQUE_ID, WEEK, 'Name',
#                    'PlayerPos', 'ActivePos', REAL_SCORE, PROJ_SCORE, 'PctPlayed']

OFFENSEANDBENCH = 0
KICKER = 1
DEFENSE = 2

TABLES = [OFFENSEANDBENCH, KICKER, DEFENSE]


class PlayerParser:
    def __init__(self):
        self.current_soup = ''
        self.data_indices = {'ActivePos': 0,
                             'Name': 1,
                             'Team': 1,
                             'PlayerPos': 1,
                             'RealScore': 5,
                             'ProjScore': 6,
                             'PctPlayed': 7}

    def get_all_info(self, soup):
        all_data = []
        for index, table in enumerate(TABLES):
            if index == 0:
                all_data = self.parse_player_table(soup, index)
            else:
                new_data = self.parse_player_table(soup, index)
                for entry in new_data:
                    all_data.append(entry)
                # all_data.append(self.parse_player_table(soup, index))
        return all_data

    def get_stat_table(self, soup, index):
        return soup.find('table', id=f'statTable{index}').find('tbody')

    def get_table_rows(self, table_soup):
        return table_soup.find_all('tr')

    def get_table_colunms(self, row_soup):
        return row_soup.find_all('td')

    def combine_all_data(self, arrays):
        out_array = []
        for index, arr in enumerate(arrays):
            if index == 0:
                out_array = arr
            else:
                out_array = out_array.extend(arr)
        return out_array

    def parse_player_table(self, soup, index):
        logger.debug(f'Parsing table index = {index}')
        stat_table = self.get_stat_table(soup, index)
        player_rows = self.get_table_rows(stat_table)
        logger.debug(f'found {len(player_rows)} rows')
        all_data = []
        for index, row in enumerate(player_rows):
            logger.debug(f'checking row {index}')
            new_data = self.parse_player(row)
            all_data.append(new_data)
        return all_data

    def parse_player(self, row_soup):
        self.current_soup = row_soup
        stat_cells = self.get_table_colunms(row_soup)
        if self.handle_forecast(stat_cells):
            logger.debug('forecast detected')

        active_position = self.get_active_pos(stat_cells[self.data_indices['ActivePos']])

        if self.is_unplayed_pos(row_soup):
            return_data = ['None', active_position, active_position, 0, 0, 0]
            return return_data
        else:
            player_position = self.get_player_pos(stat_cells[self.data_indices['PlayerPos']])

        player_name = self.get_player_name(stat_cells[self.data_indices['Name']])

        if self.is_player_on_bye(row_soup):
            return_data = [player_name, player_position, active_position, 0, 0, 0]
        else:
            real_score = self.get_real_score(stat_cells[self.data_indices['RealScore']])
            projected_score = self.get_proj_score(stat_cells[self.data_indices['ProjScore']])
            percent_start = self.get_percent_played(stat_cells[self.data_indices['PctPlayed']])
            return_data = [player_name, player_position, active_position, real_score, projected_score, percent_start]
        return return_data

    @staticmethod
    def get_active_pos(cell_soup):
        return cell_soup.find('span')['data-pos']

    @staticmethod
    def get_player_name(cell_soup):
        return cell_soup.find('a', class_='Nowrap name F-link').contents[0]

    @staticmethod
    def get_player_pos(cell_soup):
        team_pos = cell_soup.find('span', class_='Fz-xxs').contents[0]
        return team_pos.split('-')[1].strip()

    @staticmethod
    def get_team(cell_soup):
        team_pos = cell_soup.find('span', class_='Fz-xxs').contents[0]
        return team_pos.split('-')[0].strip()

    @staticmethod
    def get_real_score(cell_soup):
        return cell_soup.find('a').contents[0]

    @staticmethod
    def get_proj_score(cell_soup):
        return cell_soup.find('div').contents[0]

    @staticmethod
    def get_percent_played(cell_soup):
        return cell_soup.find('div').contents[0].strip('%')

    @staticmethod
    def is_player_on_bye(row_soup):
        if 'Bye' in str(row_soup):
            return True
        else:
            return False

    @staticmethod
    def is_unplayed_pos(row_soup):
        return 'Empty' in str(row_soup)

    def handle_forecast(self, all_cell_soup):
        if len(all_cell_soup) >= 27:
            self.shift_data_indices()
            return True
        else:
            self.reset_data_indices()
            return False

        try:
            if 'Forecast' in all_cell_soup[4].find('a').contents[0]:
                self.shift_data_indices()
                return True
            else:
                self.reset_data_indices()
                return False
        except Exception as e:
            self.reset_data_indices()
            return False

    def shift_data_indices(self):
        self.data_indices = {'ActivePos': 0,
                             'Name': 1,
                             'Team': 1,
                             'PlayerPos': 1,
                             'RealScore': 6,
                             'ProjScore': 7,
                             'PctPlayed': 8}

    def reset_data_indices(self):
        self.data_indices = {'ActivePos': 0,
                             'Name': 1,
                             'Team': 1,
                             'PlayerPos': 1,
                             'RealScore': 5,
                             'ProjScore': 6,
                             'PctPlayed': 7}

    @staticmethod
    def is_empty(row_soup):
        return '(Empty)' in str(row_soup)