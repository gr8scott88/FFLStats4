from models.League import League
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os


class LeagueVisualizer:
    def __init__(self, league_: League):
        self.league = league_
        sns.set_context('talk')

    def plot_real_score_by_week(self, save=False):
        merged = pd.merge(self.league.score_info, self.league.league_info, on='TeamID', how='left')
        grouped = merged.groupby('TeamName')
        fig, ax = plt.subplots(figsize=(15, 7))
        for name, group in grouped:
            group.plot(x='Week', y='RealScore', ax=ax, label=name)
        plot_title = f'Real Score by Week for {self.league.name}'
        plt.title(plot_title)
        plt.legend(loc='upper left')
        if save:
            self.save_plot(name)
        else:
            plt.show()

    def plot_cum_real_score_by_week(self, save=False):
        merged = pd.merge(self.league.score_info, self.league.league_info, on='TeamID', how='left')
        grouped = merged.groupby('TeamName')
        fig, ax = plt.subplots(figsize=(15, 7))
        for name, group in grouped:
            group['CumScore'] = group['RealScore'].cumsum()
            group.plot(x='Week', y='CumScore', ax=ax, label=name)
        plot_title = f'Cumulative Total Score by Week for {self.league.name}'
        plt.title(plot_title)
        plt.legend(loc='upper left')
        if save:
            self.save_plot(plot_title)
        else:
            plt.show()

    def plot_real_vs_proj_by_week(self, save=False):
        merged = pd.merge(self.league.score_info, self.league.league_info, on='TeamID', how='left')
        merged['Delta'] = merged['RealScore'] - merged['ProjScore']
        grouped = merged.groupby('TeamName')
        fig, ax = plt.subplots(figsize=(15, 7))
        for name, group in grouped:
            group.plot(x='Week', y='Delta', ax=ax, label=name)
        plot_title = f'Estimation Error by Week for {self.league.name}'
        plt.title(plot_title)
        plt.legend(loc='upper left')
        if save:
            self.save_plot(plot_title)
        else:
            plt.show()

    def plot_cum_real_vs_proj_by_week(self, save=False):
        merged = pd.merge(self.league.score_info, self.league.league_info, on='TeamID', how='left')
        merged['Delta'] = merged['RealScore'] - merged['ProjScore']
        grouped = merged.groupby('TeamName')
        fig, ax = plt.subplots(figsize=(15, 7))
        for name, group in grouped:
            group['CumDelta'] = group['Delta'].cumsum()
            group.plot(x='Week', y='CumDelta', ax=ax, label=name)
        plot_title = f'Cumulative Estimation Error by Week for {self.league.name}'
        plt.title(plot_title)
        plt.legend(loc='upper left')
        if save:
            self.save_plot(plot_title)
        else:
            plt.show()

    def plot_player_breakdown(self, save=False):
        #TODO
        pass


    @staticmethod
    def save_plot(name):
        fpath = os.path.join('plots', name)
        plt.savefig(fpath)
        plt.close()

