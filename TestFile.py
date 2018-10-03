
import TeamManager as tm
import LeagueManager as lm
import os
import pandas as pd
from bs4 import BeautifulSoup




# \venv\Scripts\activate


relative_dir = r'data\FFL_Info.csv'
# script_dir = r'C:\Users\gr8sc\PycharmProjects\FFLStats4'
script_dir = r'C:\Dev\Python\FFLStats4'
file_dir = os.path.join(script_dir, relative_dir)
print(file_dir)

week_id = 3

league_frame = lm.load_league(file_dir, week_id)

