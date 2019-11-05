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
load_thru_week = 8

AFC = League.League(AFC_id, 'AFC')
NFC = League.League(NFC_id, 'NFC')

AFC_vis = LeagueVisualizer(AFC)
NFC_vis = LeagueVisualizer(NFC)

AFC.load_team_scores_through_week(load_thru_week)
NFC.load_team_scores_through_week(load_thru_week)

AFC_vis.plot_cum_real_vs_proj_by_week()
NFC_vis.plot_cum_real_vs_proj_by_week()
