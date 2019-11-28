from models import League
from utility.YahooWebHelper import YahooWebHelper
from web_parsing.MatchPageParser import MatchParser
from web_parsing.TeamPageParser import TeamParser
from data_handlers.PandasHandler import PandasDataHandler
import matplotlib.pyplot as plt
import pandas as pd
from data_vis.LeagueVisualizer import LeagueVisualizer

helper = YahooWebHelper()
mp = MatchParser()
tp = TeamParser()
AFC_id = 609682
NFC_id = 713428
load_thru_week = 11

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


s= helper.get_soup('https://football.fantasysports.yahoo.com/f1/713428/7/team?week=11')
stat_table = s.find_all('section', {'class': 'stat-target'})[0]
sub_tables = stat_table.findChildren('div', recursive=False)
offense_and_bench = sub_tables[0]
kickers = sub_tables[1]
defense = sub_tables[2]
