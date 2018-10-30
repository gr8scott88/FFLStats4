from bs4 import BeautifulSoup
import TeamParser
import WebHelper
import GLOBALS
import Webpage
import FileManager
import os
import Player
import Helper


class Team:
    def __init__(self, league_id, team_id):
        self.league_id = league_id
        self.team_id = team_id
        self.soup = False
        self.parser = TeamParser.TeamParser()
        self.team_data = []
        self.player_data = []

    def load_soup_for_week(self, week, time):
        html_file_name = str(self.team_id) + '_' + str(time) + '.html'
        html_dir = os.path.join(str(self.league_id), 'week_' + str(week))
        loaded_html = FileManager.load_html(html_dir, html_file_name)
        if loaded_html is False:
            print('Loading HTML from website)')
            # team_url = WebHelper.build_url(GLOBALS.URLROOT, self.leaguid, self.teamid)
            team_url = WebHelper.build_url_for_week(GLOBALS.URLROOT, self.league_id, self.team_id, week)
            print(team_url)
            webpage = Webpage.Webpage(team_url)
            team_soup = webpage.get_soup()
            webpage.save_team_html(time)
        else:
            print('HTML loaded from file')
            print(os.path.join(html_dir, html_file_name))
            team_soup = BeautifulSoup(loaded_html, 'html.parser')
        self.soup = team_soup

    def load_soup_for_season(self, max_week):
        for week in range(max_week):
            for time in range(GLOBALS.MAXTIMESLICES):
                print('Week: ' + str(week) + '_Time: '+ str(time))

    def parse_team_info(self):
        if not self.soup:
            print('Soup not loaded')
            return False
        else:
            self.team_data = self.parser.parse_team_stats(self.soup)
            print(self.team_data)
            return self.team_data

    def get_team_data(self):
        print(self.team_data)
        return self.team_data

    def parse_player_info(self):
        # player_table =
        pass

    def get_players(self, player_table):
        # get players
        pass

    def get_offensive_players(self):
        # offensive_player_table = soup.find_all('table', id='statTable0')
        # offensive_players = offensive_player_table[0].find('tbody').find_all('tr')
        #for index, player in enumerate(offensive_players):
        #    # print('Parsing player: ' + str(index))
        #     all_player_info.append(help.floatify(self.parse_offensive_player(player)))

        offensive_player_table = self.soup.find_all('table', id='statTable0')
        offensive_players = offensive_player_table[0].find('tbody').find_all('tr')
        return offensive_players

    def get_kickers(self):
        kicker_table = self.soup.find_all('table', id='statTable1')
        return kicker_table[0]

    def get_defensive_players(self):
        defensive_table = self.soup.find_all('table', id='statTable2')
        return defensive_table[0]

    def parse_all_player_info(self):
        all_data = []
        offensive_players = self.get_offensive_players()
        for offensive_player_row in offensive_players:
            offensive_player = Player.Player(offensive_player_row, 'OFF')
            player_data = offensive_player.parse_player_data()
            all_data.append(player_data)

        kicker_row = self.get_kickers()
        kicker = Player.Player(kicker_row, 'KICKER')
        kicker_data = kicker.parse_player_data()
        all_data.append(kicker_data)

        defensive_row = self.get_defensive_players()
        defense = Player.Player(defensive_row, 'DEF')
        defense_data = defense.parse_player_data()
        all_data.append(defense_data)

        return Helper.player_data_float_convert(all_data)












