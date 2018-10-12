

class TeamParser:
    def __init__(self):
        pass

    def parse_team_stats(self, soup):
        team_score = float(self.get_team_score(soup))
        proj_score = float(self.get_team_projected_score(soup))
        return [team_score, proj_score]

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