import os

filepath_root = r'/data_archive'
url_root = r'https://football.fantasysports.yahoo.com/f1/'


class DataLoader:
    def __init__(self, league_id, no_teams):
        self.no_teams = no_teams
        self.league_id = league_id

    def load_data_to_date(self, week):
        for w in range(week):
            self.load_week_data(w)

    def load_week_data(self, week):
        success = self.load_local_data(week)
        if not success:
            success = self.load_web_data(week)
        if not success:
            raise RuntimeError('Unable to load data')

    def load_local_data(self, week, team):

        return True

    def load_web_data(self, week, team):

        return True

    def parse_results(self, html):
        pass

    def build_url(self, week, team):
        return f'{url_root}/{self.league_id}/{team}/team?&week={week}'

    def build_filepath(self, week, team):
        return os.path.join(filepath_root, str(self.league_id), str(week), f'{team}.html')


