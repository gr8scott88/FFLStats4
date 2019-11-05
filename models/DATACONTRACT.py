LEAGUE_ID = 'LeagueID'
LEAGUE_NAME = 'LeagueName'
TEAM_ID = 'TeamID'
TEAM_NAME = 'TeamName'

TEAMINFOCOLS = ['UniqueID', 'LeagueID', 'LeagueName', 'TeamID', 'TeamName']
TEAMSCORECOLS = ['UniqueID', 'TeamID', 'Week', 'RealScore', 'ProjScore']
PLAYERSCORECOLS = ['UniqueID', 'Week', 'Name',
                   'PlayerPos', 'ActivePos', 'RealScore', 'ProjScore', 'PctPlayed']
LEAGUEINFOCOLS = ['UniqueID', 'LeagueID', 'TeamID', 'TeamName']
LEAGUETRACKERCOLS = ['UniqueID', 'LeagueId', 'LeagueName', 'Order', 'TeamID', 'TeamName']

DATAROOT = r'data_archive'
LEAGUEFILENAME = 'LeagueInfo'
MATCHUPFILENAME = 'MatchupInfo'
SCOREFILENAME  = 'ScoreInfo'

LEAGUEHTML= 'LeagueHTML'
TEAMHTML = 'TeamHTML'
MATCHUPHTML = 'MatchupHTML'

EXPORTDIR = 'export'