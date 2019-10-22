from models import League
from utility.YahooWebHelper import YahooWebHelper

helper = YahooWebHelper()

AFC_id = 609682

AFC = League.League(AFC_id)
