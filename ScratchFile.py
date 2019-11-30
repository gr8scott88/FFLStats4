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

AFC.load_all_player_data_through_week(load_thru_week)
NFC.load_all_player_data_through_week(load_thru_week)

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
