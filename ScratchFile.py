from models import League
from utility.YahooWebHelper import YahooWebHelper
from web_parsing.MatchPageParser import MatchParser
from web_parsing.TeamPageParser import TeamParser
from web_parsing.PlayerParser import PlayerParser
from data_handlers.PandasHandler import PandasDataHandler
import matplotlib.pyplot as plt
import pandas as pd
from data_vis.LeagueVisualizer import LeagueVisualizer

helper = YahooWebHelper()
mp = MatchParser()
tp = TeamParser()
AFC_id = 609682
NFC_id = 713428
load_thru_week = 12

AFC = League.League(AFC_id, 'AFC')
NFC = League.League(NFC_id, 'NFC')

AFC.load_team_scores_through_week(load_thru_week)
NFC.load_team_scores_through_week(load_thru_week)

AFC_vis = LeagueVisualizer(AFC)
NFC_vis = LeagueVisualizer(NFC)

AFC_vis.plot_cum_real_vs_proj_by_week(save=True)
NFC_vis.plot_cum_real_vs_proj_by_week(save=True)

AFC_vis.plot_cum_real_score_by_week(save=True)
NFC_vis.plot_cum_real_score_by_week(save=True)

AFC_vis.plot_real_score_by_week(save=True)
NFC_vis.plot_real_score_by_week(save=True)

AFC_vis.plot_real_vs_proj_by_week(save=True)
NFC_vis.plot_real_vs_proj_by_week(save=True)


pp = PlayerParser()
s = helper.get_soup('https://football.fantasysports.yahoo.com/f1/713428/7/team?week=11')
res = pp.get_all_player_info(s)

stat_table = s.find_all('section', {'class': 'stat-target'})[0]
sub_tables = stat_table.findChildren('div', recursive=False)
offense_and_bench_table = sub_tables[0]
kicker_table = sub_tables[1]
defense_table = sub_tables[2]
offense_and_bench_players = pp.get_all_offensive_and_bench_players(offense_and_bench_table)
defense_players = pp.get_all_defense_info(defense_table)
kicker_players = pp.get_all_kicker_info(kicker_table)


off_rows = offense_and_bench.find_all('tr')


