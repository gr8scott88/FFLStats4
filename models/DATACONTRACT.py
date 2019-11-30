LEAGUE_ID = 'LeagueID'
UNIQUE_ID = 'UniqueID'
LEAGUE_NAME = 'LeagueName'
TEAM_ID = 'TeamID'
TEAM_NAME = 'TeamName'
REAL_SCORE = 'RealScore'
PROJ_SCORE = 'ProjScore'
WEEK = 'Week'
SLOT = 'Slot'
ACTIVEPOS = 'ActivePos'
PCTSTART = 'PctStart'
PLAYERNAME = 'PlayerName'
TEAMRANKING = 'Ranking'

TEAMINFOCOLS = [UNIQUE_ID, LEAGUE_ID, LEAGUE_NAME, TEAM_ID, TEAM_NAME]
TEAMSCORECOLS = [UNIQUE_ID, TEAM_ID, WEEK, REAL_SCORE, PROJ_SCORE]
PLAYERSCORECOLS = [UNIQUE_ID, WEEK, PLAYERNAME,
                   SLOT, ACTIVEPOS, REAL_SCORE, PROJ_SCORE, PCTSTART]
PLAYERPARSECOLS = [PLAYERNAME, SLOT, ACTIVEPOS, REAL_SCORE, PROJ_SCORE, PCTSTART]
LEAGUEINFOCOLS = [UNIQUE_ID, LEAGUE_ID, TEAM_ID, TEAM_NAME]
LEAGUETRACKERCOLS = [UNIQUE_ID, LEAGUE_ID, LEAGUE_NAME, 'Order', TEAM_ID, TEAM_NAME]
RANKINGTRACKERCOLS = [UNIQUE_ID, LEAGUE_ID, TEAM_ID, TEAM_NAME, WEEK, TEAMRANKING]

DATAROOT = r'data_archive'
LEAGUEFILENAME = 'LeagueInfo'
MATCHUPFILENAME = 'MatchupInfo'
SCOREFILENAME = 'ScoreInfo'
PLAYERFILENAME = 'PlayerInfo'

LEAGUEHTML= 'LeagueHTML'
TEAMHTML = 'TeamHTML'
MATCHUPHTML = 'MatchupHTML'

EXPORTDIR = 'export'
PLAYERREPORTS = 'player_reports'
LEAGUEREPORTS = 'league_reports'
