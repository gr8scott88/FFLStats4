from bs4 import BeautifulSoup
import TeamParser as tp
import DATACONTRACT


class Team:
    def __init__(self, league):
        self.parser = tp.PlayerParser()
        self.league = league

    def get_team_info(self, unique_id):
        soup = self.get_soup(unique_id)
        all_data = self.parse_all_stats(soup, unique_id)
        return all_data

    def get_soup(self, unique_id):
        # Refactor
        current_html = self.data_manager.load_or_download_html(unique_id)
        soup = BeautifulSoup(current_html, 'html.parser')
        return soup

    def parse_all_stats(self, soup, unique_id):
        team_stats = self.data_parser.parse_team_stats(soup)
        player_stats = self.data_parser.parse_player_stats(soup)
        # team_stats = self.parse_team_stats(soup)
        # player_stats = self.parse_player_stats(soup)
        return [unique_id.get_id_array(), team_stats, player_stats]

