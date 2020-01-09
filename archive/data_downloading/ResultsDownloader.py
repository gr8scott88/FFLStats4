import requests
import os


file_root = r'/'


class ResultsDownloader:
    def __init__(self, league_id, no_teams):
        self.url_root = 'https://football.fantasysports.yahoo.com/f1/'
        self.league_id = league_id
        self.no_teams = no_teams

    def download_all_current(self, current_week):
        for week in range(current_week):
            self.download_week(week)

    def download_week(self, week):
        for team in range(self.no_teams):
            self.download_team(team + 1, week)

    def download_team(self, team, week):
        url = f'{self.url_root}/{self.league_id}/{team}/team?&week={week}'
        # print(url)
        page = requests.get(url)
        # print(page)
        folder_path = os.path.join(file_root, 'data_archive', str(self.league_id), str(week))

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, f'{team}_results.html')
        with open(file_path, 'wb') as f:
            f.write(str(page.content).encode('utf-8'))


