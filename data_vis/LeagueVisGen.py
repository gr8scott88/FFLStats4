from models.League import League
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
from matplotlib.cm import get_cmap
from models import DATACONTRACT
import numpy as np


color_wheel = "Accent"
cmap = get_cmap(color_wheel)
colors = cmap.colors


def plot_real_score_by_week(league: League, save=False):
    merged = pd.merge(league.score_info, league.league_info, on='TeamID', how='left')
    grouped = merged.groupby('TeamName')
    fig, ax = plt.subplots(figsize=(15, 7))
    name = 'null'
    for name, group in grouped:
        group.plot(x='Week', y='RealScore', ax=ax, label=name)
    plot_title = f'Real Score by Week for {league.name}'
    plt.title(plot_title)
    plt.legend(loc='upper left')
    if save:
        save_plot(league, plot_title)
    else:
        plt.show()


def plot_cum_real_score_by_week(league: League, save=False):
    merged = pd.merge(league.score_info, league.league_info, on='TeamID', how='left')
    grouped = merged.groupby('TeamName')
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set_prop_cycle(color=colors)
    for name, group in grouped:
        group['CumScore'] = group['RealScore'].cumsum()
        group.plot(x='Week', y='CumScore', ax=ax, label=name)
    plot_title = f'Cumulative Total Score by Week for {league.name}'
    plt.title(plot_title)
    plt.legend(loc='upper left')

    if save:
        save_plot(league, plot_title)
    else:
        plt.show()


def plot_real_vs_proj_by_week(league: League, save=False):
    merged = pd.merge(league.score_info, league.league_info, on='TeamID', how='left')
    merged['Delta'] = merged['RealScore'] - merged['ProjScore']
    grouped = merged.groupby('TeamName')
    fig, ax = plt.subplots(figsize=(15, 7))
    for name, group in grouped:
        group.plot(x='Week', y='Delta', ax=ax, label=name)
    plot_title = f'Estimation Error by Week for {league.name}'
    plt.title(plot_title)
    plt.legend(loc='upper left')
    if save:
        save_plot(league, plot_title)
    else:
        plt.show()


def plot_cum_real_vs_proj_by_week(league: League, save=False):
    merged = pd.merge(league.score_info, league.league_info, on='TeamID', how='left')
    merged['Delta'] = merged['RealScore'] - merged['ProjScore']
    grouped = merged.groupby('TeamName')
    fig, ax = plt.subplots(figsize=(15, 7))
    for name, group in grouped:
        group['CumDelta'] = group['Delta'].cumsum()
        group.plot(x='Week', y='CumDelta', ax=ax, label=name)
    plot_title = f'Cumulative Estimation Error by Week for {league.name}'
    plt.title(plot_title)
    plt.legend(loc='upper left')
    if save:
        save_plot(league, plot_title)
    else:
        plt.show()


def plot_player_breakdown_for_all_teams(league: League, save=False):
    teams = league.player_info.groupby('UniqueID')
    for team in teams:
        plot_player_breakdown_by_team_var(league, team, save)


def plot_player_breakdown_by_team(league: League, team, save=False):
    team_df = team[1]
    team_name = league.league_info.loc[league.league_info['UniqueID'] == team[0], 'TeamName'].iloc[0]
    filtered = team_df.loc[~team_df['ActivePos'].isin(['BN'])]
    grouped = filtered.groupby(['UniqueID', 'Week', 'ActivePos'])['RealScore'].sum().unstack('ActivePos')
    grouped.plot(kind='bar', stacked=True)
    plot_title = f'Score Breakdown by Position for {team_name}'
    plt.title(plot_title)
    if save:
        save_plot(league, plot_title)
    else:
        plt.show()


def plot_player_breakdown_by_team_var(league: League, team, save=False):
    team_df = team[1]
    team_name = league.league_info.loc[league.league_info['UniqueID'] == team[0], 'TeamName'].iloc[0]
    filtered = team_df.loc[~team_df['ActivePos'].isin(['BN', 'IR'])]
    grouped_by_id = filtered.groupby(['UniqueID'])
    for name, group in grouped_by_id:
        f = plt.figure(figsize=(20, 10))
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
            save_plot(league, plot_title)
        else:
            plt.show()


def plot_player_breakdown_for_season(league: League, save=False):
    f, ax = plt.subplots(figsize=(20, 10))
    ax.set_prop_cycle(color=colors)
    df = pd.merge(league.player_info, league.league_info, on='UniqueID')
    filtered = df.loc[~df['ActivePos'].isin(['BN', 'IR'])]
    grouped = filtered.groupby(['TeamName', 'ActivePos'])['RealScore'].sum().unstack('ActivePos')
    grouped.plot(kind='bar', stacked=True, ax=f.gca())
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plot_title = f'Score Breakdown by Position for {league.name}'
    plt.title(plot_title)
    f.subplots_adjust(right=0.8)
    f.subplots_adjust(bottom=0.3)
    plt.xticks(rotation=30, ha='right')
    if save:
        plt.show()
        save_plot(league, plot_title)
    else:
        plt.show()



def plot_draft_value_by_team(league: League, max_draft, thru_week: int, save=False):
    # f, ax = plt.subplots(figsize=(20, 10))
    league.draft_info[DATACONTRACT.DRAFTORDER] = pd.to_numeric(league.draft_info[DATACONTRACT.DRAFTORDER])
    # league.player_info.join(league.draft_info, on=DATACONTRACT.PLAYERNAME)
    data = league.player_info.merge(league.draft_info[[DATACONTRACT.DRAFTORDER, DATACONTRACT.PLAYERNAME]],
                                    on=DATACONTRACT.PLAYERNAME)

    order_filter = f'{DATACONTRACT.DRAFTORDER}<={max_draft}'
    week_filter = f'{DATACONTRACT.WEEK}<={thru_week}'
    filtered = data.query(order_filter)
    filtered = filtered.query(week_filter)
    draft_scores = filtered.groupby(DATACONTRACT.UNIQUE_ID)[DATACONTRACT.REAL_SCORE].sum()
    draft_scores = draft_scores.to_frame().reset_index()
    cleaned = draft_scores.merge(league.league_info[[DATACONTRACT.UNIQUE_ID, DATACONTRACT.TEAM_NAME]],
                                 on=DATACONTRACT.UNIQUE_ID)
    cleaned = cleaned.set_index(DATACONTRACT.TEAM_NAME)
    # plot = cleaned.plot.pie(y=DATACONTRACT.REAL_SCORE, figsize=(15, 10), legend='', autopct='%1.1f%%')
    plot = cleaned.plot.pie(y=DATACONTRACT.REAL_SCORE, figsize=(15, 10), legend='',
                            autopct=lambda val: np.round(val / 100. * cleaned[DATACONTRACT.REAL_SCORE].sum(), 0))
    plot_title = f'Cumulative Score from Top {max_draft} Drafted Players for {league.name} Through Week {thru_week}'
    plt.title(plot_title)
    plt.ylabel('')
    if save:
        plt.show()
        save_plot(league, plot_title)
    else:
        plt.show()


def save_plot(league: League, name):
    name = name.replace('.', '')
    dir_path = os.path.join('export', 'plots', league.name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    fpath = os.path.join('export', 'plots', league.name, name)
    plt.savefig(fpath)
    plt.close()
