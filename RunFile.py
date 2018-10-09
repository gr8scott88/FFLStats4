import SeasonManager as sm
import DataManager as dm
import DataParser as dp
import Helper
import StatManager as stat
import matplotlib as plt
import os



# script_dir = r'C:\Users\gr8sc\PycharmProjects\FFLStats4'
script_dir = r'C:\Dev\Python\Projects\FFLStats4'

data_manager = dm.DataManager(script_dir)
season_manager = sm.SeasonManager(data_manager)
parser = dp.DataParser()

season_manager.load_single_week_data(5)

# season_manager.load_all_season_data(5)


data_manager.quick_export()





pd = data_manager.player_frame
wk5_players = pd.loc[pd['Week'] == 5.0]
wk5_WRs = wk5_players.loc[wk5_players['ActivePos'] == 'WR']
# wk5_WRs.groupby(['League', 'Team'])
ans = wk5_WRs.groupby(['LeagueID', 'TeamID']).max()
ans['RealScore']