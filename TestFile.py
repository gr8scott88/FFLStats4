import League
import DataManager

nfc_id = 729457
nfc_data = DataManager.DataManager()
NFC = League.League(nfc_id, nfc_data)
NFC.load_all_data_points(8)
nfc_data.export_complete_team_frame(nfc_id)

afc_id = 910981
afc_data = DataManager.DataManager()
AFC = League.League(afc_id, afc_data)
AFC.load_all_data_points(8)
afc_data.export_complete_team_frame(afc_id)
