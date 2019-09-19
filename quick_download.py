from data_downloading import ResultsDownloader as rd


results = rd.ResultsDownloader(609682, 10)
# results.download_team(1, 1)
results.download_all_current(12)


results = rd.ResultsDownloader(713428, 10)
results.download_all_current(12)


