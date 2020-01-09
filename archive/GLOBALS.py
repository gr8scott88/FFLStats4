import os

ROOTDIR = r'C:\Dev\Python\Projects\FFLStats4'
try:
    ROOTDIR = os.path.dirname(os.path.realpath(__file__))
except Exception as e:
    print('Script not being run dynamically')
URLROOT = r'https://football.fantasysports.yahoo.com/f1/'

MAXTIMESLICES = 20

