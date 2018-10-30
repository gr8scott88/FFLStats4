import PlayerParser


class Player:
    def __init__(self, player_row, player_type):
        self.parser = PlayerParser.PlayerParser()
        self.soup = player_row
        self.type = player_type

    def parse_player_data(self):
        player_data = []
        if self.type == 'OFF':
            player_data = self.parse_offensive_info()
        elif self.type == 'KICKER':
            player_data = self.parse_kicker_info()
        elif self.type == 'DEF':
            player_data = self.parse_defensive_info()
        else:
            print('Invalid player type')
        return player_data

    def parse_offensive_info(self):
        return self.parser.parse_offensive_player(self.soup)

    def parse_kicker_info(self):
        return self.parser.parse_kicker(self.soup)

    def parse_defensive_info(self):
        return self.parser.parse_defense(self.soup)
