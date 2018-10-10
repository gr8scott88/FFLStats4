import SeasonManager as sm
import DataManager as dm
import DataParser as dp
import StatManager as stat

# script_dir = r'C:\Users\gr8sc\PycharmProjects\FFLStats4'
script_dir = r'C:\Dev\Python\Projects\FFLStats4'

data_manager = dm.DataManager(script_dir)
season_manager = sm.SeasonManager(data_manager)
parser = dp.DataParser()

season_manager.load_single_week_data(5)

stats = stat.StatManager(data_manager)

TD = data_manager.team_frame
PD = data_manager.player_frame

WRSum_5 = stats.cum_sum_position_by_week('WR', 5)
WRSum_5.to_csv('WRSum_5.csv')

QBMax_5 = stats.max_score_position_by_week('QB', 5)


# season_manager.load_all_season_data(5)


data_manager.quick_export()





pd = data_manager.player_frame
wk5_players = pd.loc[pd['Week'] == 5.0]
wk5_WRs = wk5_players.loc[wk5_players['ActivePos'] == 'WR']
# wk5_WRs.groupby(['League', 'Team'])
ans = wk5_WRs.groupby(['LeagueID', 'TeamID', 'TeamOrder']).sum()
ans['RealScore']