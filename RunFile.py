from models import League
from utility import DataManager
import configparser

# currentWeek = 12
targetWeek = 1

config = configparser.ConfigParser()
config.read(r'config/config.ini')
for key in config['LEAGUES']:
    print(key)
    if 'afc' in key:
        afc_id = config['LEAGUES'][key]
    elif 'nfc'in key:
        nfc_id = config['LEAGUES'][key]


# afc_id = 609682
afc_data = DataManager.DataManager()
AFC = League.League(afc_id, afc_data)
# AFC.load_all_data_points(currentWeek)
AFC.load_data_point(targetWeek, 0)
# afc_data.export_complete_team_frame(afc_id)


# nfc_id = 713428
nfc_data = DataManager.DataManager()
NFC = League.League(nfc_id, nfc_data)
# NFC.load_all_data_points(currentWeek)
NFC.load_data_point(targetWeek, 0)
# nfc_data.export_complete_team_frame(nfc_id)






r = nfc_data.cum_sum_position_by_week("BN", targetWeek)
# nfc_data.export_dataframe(r, 'NFC_Contest_Week_' + str(targetWeek))

r2 = nfc_data.max_score_position_by_week("WR", targetWeek)


r = afc_data.cum_sum_position_by_week("BN", targetWeek)
afc_data.export_dataframe(r, 'AFC_Contest_Week_' + str(targetWeek))


