

class MatchParser:
    def __init__(self):
        pass

    def get_opponent(self, match_page_soup):
        header = match_page_soup.find_all('section', {'id': 'matchup-header'})[0]
        opponent_box = header.find_all('div', {'class': 'Fz-xxl Ell'})[1]
        opp_href = opponent_box.find('a').get('href')
        opponent_id = self.get_id_from_href(opp_href)
        return opponent_id

    @staticmethod
    def get_id_from_href(href):
        arr = href.split('/')
        opponent_id = arr[-1]
        return opponent_id
