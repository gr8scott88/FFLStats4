from web_parsing.PlayerParser import PlayerParser
from utility.YahooWebHelper import YahooWebHelper
helper = YahooWebHelper()

pp = PlayerParser()
url = r'https://football.fantasysports.yahoo.com/f1/713428/7/team?week=11'
# url = r'https://football.fantasysports.yahoo.com/f1/609682/9/team?&week=4'
soup = helper.get_soup(url)
# res = pp.get_all_player_info(soup)
res = pp.get_all_info(soup)


ot = pp.get_stat_table(soup, 0)
rows = pp.get_table_rows(ot)
emptyplayer = pp.get_table_colunms(rows[2])



