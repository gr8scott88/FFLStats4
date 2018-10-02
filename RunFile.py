
import TeamManager as dm

# \venv\Scripts\activate

# loaded_team_info = pd.read_csv('FFL_Info.csv')
# url = r"week3test.html"

ex_url = 'https://football.fantasysports.yahoo.com/f1/910981/4/team?&week=3'
ex_saved_html = r'week3test.html'

# get_all_info(team_info)


league = '910981'
team = '4'
week = '3'
# loaded_soup = get_soup_single(league, team, week)

loaded_soup = dm.load_soup_single(ex_saved_html)
all_week_info = dm.get_player_info(loaded_soup)


for player in all_week_info:
    print(player)