from models import League
from models import DATACONTRACT
from utility.YahooWebHelper import YahooWebHelper
from web_parsing.MatchPageParser import MatchParser
from web_parsing.TeamPageParser import TeamParser
from web_parsing.PlayerParser import PlayerParser
from data_handlers.PandasHandler import PandasDataHandler
import matplotlib.pyplot as plt
import pandas as pd
from data_vis.LeagueVisualizer import LeagueVisualizer
import numpy as np

helper = YahooWebHelper()
mp = MatchParser()
tp = TeamParser()
AFC_id = 609682
NFC_id = 713428
load_thru_week = 12

AFC = League.League(AFC_id, 'AFC')
NFC = League.League(NFC_id, 'NFC')
AFC_vis = LeagueVisualizer(AFC)
NFC_vis = LeagueVisualizer(NFC)

AFC.player_info.join(AFC.draft_info, on=DATACONTRACT.PLAYERNAME)

# df["y"] = pd.to_numeric(df["y"])
AFC.draft_info[DATACONTRACT.DRAFTORDER] = pd.to_numeric(AFC.draft_info[DATACONTRACT.DRAFTORDER])

data = AFC.player_info.merge(AFC.draft_info[[DATACONTRACT.DRAFTORDER, DATACONTRACT.PLAYERNAME]], on=DATACONTRACT.PLAYERNAME)

# df[(df.A == 1) & (df.D == 6)]
order = 1
order_filter = f'{DATACONTRACT.DRAFTORDER}<={order}'
filtered = data.query(order_filter)
# grouped = df.groupby('A')
# >>> grouped.filter(lambda x: x['B'].mean() > 3.)
draft_scores = filtered.groupby(DATACONTRACT.UNIQUE_ID)[DATACONTRACT.REAL_SCORE].sum()
draft_scores = draft_scores.to_frame().reset_index()
# AFC.league_info[DATACONTRACT.PLAYERNAME]
cleaned = draft_scores.merge(AFC.league_info[[DATACONTRACT.UNIQUE_ID, DATACONTRACT.TEAM_NAME]], on=DATACONTRACT.UNIQUE_ID)
cleaned = cleaned.set_index(DATACONTRACT.TEAM_NAME)
# cleaned = draft_scores.join(AFC.league_info[[DATACONTRACT.UNIQUE_ID, DATACONTRACT.PLAYERNAME]], on=DATACONTRACT.UNIQUE_ID)
plot = cleaned.plot.pie(y=DATACONTRACT.REAL_SCORE, figsize=(5, 5))



def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} g)".format(pct, absolute)


f, ax = plt.subplots(figsize=(20, 10))
AFC.draft_info[DATACONTRACT.DRAFTORDER] = pd.to_numeric(AFC.draft_info[DATACONTRACT.DRAFTORDER])
# AFC.player_info.join(AFC.draft_info, on=DATACONTRACT.PLAYERNAME)
data = AFC.player_info.merge(AFC.draft_info[[DATACONTRACT.DRAFTORDER, DATACONTRACT.PLAYERNAME]],
                                on=DATACONTRACT.PLAYERNAME)
order_filter = f'{DATACONTRACT.DRAFTORDER}<={5}'
filtered = data.query(order_filter)
draft_scores = filtered.groupby(DATACONTRACT.UNIQUE_ID)[DATACONTRACT.REAL_SCORE].sum()
draft_scores = draft_scores.to_frame().reset_index()
cleaned = draft_scores.merge(AFC.league_info[[DATACONTRACT.UNIQUE_ID, DATACONTRACT.TEAM_NAME]],
                             on=DATACONTRACT.UNIQUE_ID)
cleaned = cleaned.set_index(DATACONTRACT.TEAM_NAME)
plot = cleaned.plot.pie(ax=ax, y=DATACONTRACT.REAL_SCORE, figsize=(20, 10),  autopct='%1.1f%%')
wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))
plt.setp(autotexts, size=8, weight="bold")
# plot = cleaned.plot.pie(y=DATACONTRACT.REAL_SCORE)
plt.legend(loc='center left', bbox_to_anchor=(1.2, 0.5))
plt.ylabel('')
plt.title('Title')
f.subplots_adjust(right=1.0)
f.subplots_adjust(bottom=0.3)



AFC.load_all_player_data_through_week(load_thru_week)
NFC.load_all_player_data_through_week(load_thru_week)
AFC.load_team_scores_through_week(load_thru_week)
NFC.load_team_scores_through_week(load_thru_week)


AFC_vis.plot_player_breakdown_for_season()
AFC_vis.plot_player_breakdown_for_season(save=True)
NFC_vis.plot_player_breakdown_for_season(save=True)

AFC_vis.plot_player_breakdown_for_all_teams(save=True)
NFC_vis.plot_player_breakdown_for_all_teams(save=True)


AFC_vis.plot_cum_real_vs_proj_by_week(save=True)
NFC_vis.plot_cum_real_vs_proj_by_week(save=True)


AFC_vis.plot_cum_real_score_by_week()
AFC_vis.plot_cum_real_score_by_week(save=True)
NFC_vis.plot_cum_real_score_by_week(save=True)

AFC_vis.plot_real_score_by_week(save=True)
NFC_vis.plot_real_score_by_week(save=True)

AFC_vis.plot_real_vs_proj_by_week(save=True)
NFC_vis.plot_real_vs_proj_by_week(save=True)

AFC_vis.plot_player_breakdown_for_all_teams(save=True)



# Export Scores (unfriendly format)
AFC.score_info.sort_values(['Week', 'TeamID']).to_csv('AFC_Scores.csv')
NFC.score_info.sort_values(['Week', 'TeamID']).to_csv('NFC_Scores.csv')