from utility.YahooWebHelper import YahooWebHelper
from data_storage.LocalDataManager import LocalDataManager


webHelper = YahooWebHelper()
dataHandler= LocalDataManager()

testSoup = webHelper.get_soup(r'https://football.fantasysports.yahoo.com/f1/609682')

testSoup
