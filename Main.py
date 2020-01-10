import configparser
from datetime import datetime
import math
from data_vis.LeagueVisGen import *
from models.League import League


config = configparser.ConfigParser()
config.read('config.ini')

start_week = config['Season']['StartWeek']

dt = datetime.strptime(start_week, '%m/%d/%y')
td = datetime.today()
elapsed = td - dt
current_week = math.floor(elapsed.days/7)

current_week = 16 if current_week > 16 else current_week  # cap at 16

AFC_id = config['AFC']['id']
NFC_id = config['NFC']['id']

AFC = League(AFC_id, 'AFC')
NFC = League(NFC_id, 'NFC')

AFC.update(current_week)
NFC.update(current_week)


# plot_cum_real_score_by_week(AFC)
# plot_player_breakdown_for_all_teams(AFC)
# plot_player_breakdown_for_season(AFC)

should_save = True

plot_draft_value_by_team(AFC, 5, 12, save=should_save)
plot_draft_value_by_team(NFC, 5, 12, save=should_save)

plot_cum_real_score_by_week(AFC, save=should_save)
plot_cum_real_score_by_week(NFC, save=should_save)

plot_cum_real_vs_proj_by_week(AFC, save=should_save)
plot_cum_real_vs_proj_by_week(NFC, save=should_save)


AFC.score_info[DATACONTRACT.LEAGUE_NAME] = 'AFC'
NFC.score_info[DATACONTRACT.LEAGUE_NAME] = 'NFC'
Total_DF = AFC.score_info.append(NFC.score_info)

plot_real_score_by_league_through_week(Total_DF, 5, save=should_save)
plot_cum_real_score_by_league_through_week(Total_DF, 5, save=should_save)
# Total_DF.sort_values(by=['Week'])
# g = Total_DF.groupby(['League', 'Week'])['RealScore'].sum().unstack('League')
# g.plot()
