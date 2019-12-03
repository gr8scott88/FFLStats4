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

    def plot_player_breakdown_for_all_teams(self, save=False):
        teams = self.league.player_info.groupby('UniqueID')
        for team in teams:
            self.plot_player_breakdown_by_team_var(team, save)

    def plot_player_breakdown_by_team(self, team, save=False):
        team_df = team[1]
        team_name = self.league.league_info.loc[self.league.league_info['UniqueID'] == team[0], 'TeamName'].iloc[0]
        filtered = team_df.loc[~team_df['ActivePos'].isin(['BN'])]
        grouped = filtered.groupby(['UniqueID', 'Week', 'ActivePos'])['RealScore'].sum().unstack('ActivePos')
        grouped.plot(kind='bar', stacked=True)
        plot_title = f'Score Breakdown by Position for {team_name}'
        plt.title(plot_title)
        if save:
            self.save_plot(plot_title)
        else:
            plt.show()

    def plot_player_breakdown_by_team_var(self, team, save=False):
        team_df = team[1]
        team_name = self.league.league_info.loc[self.league.league_info['UniqueID'] == team[0], 'TeamName'].iloc[0]
        filtered = team_df.loc[~team_df['ActivePos'].isin(['BN', 'IR'])]
        grouped_by_id = filtered.groupby(['UniqueID'])
        for name, group in grouped_by_id:
            f = plt.figure(figsize=(20,10))
            grouped = group.groupby(['Week', 'ActivePos'])['RealScore'].sum().unstack('ActivePos')
            grouped.plot(kind='bar', stacked=True, ax=f.gca())
            # legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plot_title = f'Score Breakdown by Position for {team_name}'
            plt.title(plot_title)
            plt.ylim(0, 200)
            plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
            f.subplots_adjust(right=0.8)
            # mng = plt.get_current_fig_manager()
            # mng.window.state('zoomed')
            if save:
                plt.show()
                self.save_plot(plot_title)
            else:
                plt.show()

    def plot_player_breakdown_for_season(self, save=False):
        f = plt.figure(figsize=(20, 10))
        df = pd.merge(self.league.player_info,self.league.league_info, on='UniqueID')
        filtered = df.loc[~df['ActivePos'].isin(['BN', 'IR'])]
        grouped = filtered.groupby(['TeamName', 'ActivePos'])['RealScore'].sum().unstack('ActivePos')
        grouped.plot(kind='bar', stacked=True, ax=f.gca())
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
        plot_title = f'Score Breakdown by Position for {self.league.name}'
        plt.title(plot_title)
        f.subplots_adjust(right=0.8)
        f.subplots_adjust(bottom=0.3)
        plt.xticks(rotation=30, ha='right')
        if save:
            plt.show()
            self.save_plot(plot_title)
        else:
            plt.show()

    def save_plot(self, name):
        name = name.replace('.', '')
        dir_path = os.path.join('plots', self.league.name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        fpath = os.path.join('plots', self.league.name, name)
        plt.savefig(fpath)
        plt.close()

