
import Team as tm
import League as lm
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests


url = r'https://football.fantasysports.yahoo.com/f1/910981'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

t = soup.find_all('ul', class_='List-rich')
p = t[0].find_all('a', class_='F-link')


import League
lid = 910981
l = League.League(lid)