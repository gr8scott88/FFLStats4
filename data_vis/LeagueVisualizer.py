from models.League import League
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class LeagueVisualizer:
    def __init__(self, league_: League):
        self.league = league_
        sns.set_context('talk')

    def plot_real_score_by_week(self):
        merged = pd.merge(self.league.score_info, self.league.league_info, on='TeamID', how='left')
        grouped = merged.groupby('TeamName')
        fig, ax = plt.subplots(figsize=(15, 7))
        for name, group in grouped:
            group.plot(x='Week', y='RealScore', ax=ax, label=name)
        plt.title(f'Real Score by Week for {self.league.name}')
        plt.show()

    def plot_real_vs_proj_by_week(self):
        merged = pd.merge(self.league.score_info, self.league.league_info, on='TeamID', how='left')
        merged['Delta'] = merged['RealScore'] - merged['ProjScore']
        grouped = merged.groupby('TeamName')
        fig, ax = plt.subplots(figsize=(15, 7))
        for name, group in grouped:
            group.plot(x='Week', y='Delta', ax=ax, label=name)
        plt.title(f'Estimation Error by Week for {self.league.name}')
        plt.show()

    def plot_cum_real_vs_proj_by_week(self):
        merged = pd.merge(self.league.score_info, self.league.league_info, on='TeamID', how='left')
        merged['Delta'] = merged['RealScore'] - merged['ProjScore']
        grouped = merged.groupby('TeamName')
        fig, ax = plt.subplots(figsize=(15, 7))
        for name, group in grouped:
            group['CumDelta'] = group['Delta'].cumsum()
            group.plot(x='Week', y='CumDelta', ax=ax, label=name)
        plt.title(f'Cumulative Estimation Error by Week for {self.league.name}')
        plt.show()

