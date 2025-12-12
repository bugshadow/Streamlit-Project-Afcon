"""
Visualization module for AFCON dashboard
Contains all plotting functions using Plotly
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# BEAUTIFUL VIBRANT COLOR SCHEME
COLOR_PALETTE = {
    'primary': '#00F260',      # Vibrant Green
    'secondary': '#0575E6',    # Electric Blue
    'accent': '#F7B801',       # Gold
    'success': '#2ECC71',      # Green
    'danger': '#E74C3C',       # Red
    'purple': '#667eea',       # Purple
    'dark': '#0a0e27',
    'light': '#ECF0F1'
}

# Vibrant color palette for charts
COLORS = [
    '#00F260', '#0575E6', '#F7B801', '#2ECC71', 
    '#E74C3C', '#667eea', '#3498DB', '#1ABC9C',
    '#F39C12', '#D35400', '#C0392B', '#8E44AD',
    '#16A085', '#27AE60', '#2980B9', '#9B59B6'
]


def apply_custom_theme(fig, title=None):
    """Apply beautiful dark theme to plotly figures with white titles"""
    fig.update_layout(
        title=title,
        title_font_size=22,
        title_font_color='white',  # WHITE TITLES
        title_font_family='Poppins, sans-serif',
        title_font_weight=600,
        font=dict(family="Poppins, sans-serif", size=13, color='white'),
        plot_bgcolor='rgba(10, 14, 39, 0.5)',  # Dark transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent
        hovermode='closest',
        showlegend=True,
        legend=dict(
            bgcolor='rgba(26, 29, 58, 0.9)',
            bordercolor='rgba(0, 242, 96, 0.3)',
            borderwidth=1,
            font=dict(color='white')
        )
    )
    
    # Grid styling with vibrant green tint
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(0, 242, 96, 0.15)',
        color='white'
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(0, 242, 96, 0.15)',
        color='white'
    )
    
    return fig


# ============ BAR CHARTS ============

def plot_team_values(team_stats_df, top_n=None):
    """Bar chart of squad values by team"""
    df = team_stats_df.copy()
    
    if top_n:
        df = df.nlargest(top_n, 'squad_value')
    
    df = df.sort_values('squad_value', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['team_name'],
        x=df['squad_value'] / 1_000_000,  # Convert to millions
        orientation='h',
        marker_color=COLOR_PALETTE['primary'],
        text=df['squad_value'].apply(lambda x: f'€{x/1_000_000:.1f}M'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Valeur: €%{x:.1f}M<extra></extra>'
    ))
    
    fig = apply_custom_theme(fig, 'Valeur des Équipes (en millions €)')
    fig.update_layout(
        xaxis_title='Valeur (Millions €)',
        yaxis_title='Équipe',
        height=max(400, len(df) * 30)
    )
    
    return fig


def plot_goals_by_team(team_stats_df):
    """Bar chart of goals scored by team"""
    df = team_stats_df.sort_values('goals_scored', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['team_name'],
        x=df['goals_scored'],
        orientation='h',
        marker_color=COLOR_PALETTE['success'],
        text=df['goals_scored'],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Buts: %{x}<extra></extra>'
    ))
    
    fig = apply_custom_theme(fig, 'Buts Marqués par Équipe')
    fig.update_layout(
        xaxis_title='Nombre de Buts',
        yaxis_title='Équipe',
        height=max(400, len(df) * 30)
    )
    
    return fig


def plot_top_scorers(player_stats_df, top_n=15):
    """Bar chart of top goal scorers"""
    df = player_stats_df[player_stats_df['goals'] > 0].copy()
    df = df.nlargest(top_n, 'goals').sort_values('goals', ascending=True)
    
    # Create labels with player name and team
    df['label'] = df['player_name'] + ' (' + df['team'] + ')'
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['label'],
        x=df['goals'],
        orientation='h',
        marker_color=COLOR_PALETTE['accent'],
        text=df['goals'],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Buts: %{x}<extra></extra>'
    ))
    
    fig = apply_custom_theme(fig, f'Top {top_n} Buteurs')
    fig.update_layout(
        xaxis_title='Nombre de Buts',
        yaxis_title='Joueur',
        height=max(400, top_n * 30)
    )
    
    return fig


def plot_top_assists(player_stats_df, top_n=15):
    """Bar chart of top assist providers"""
    df = player_stats_df[player_stats_df['assists'] > 0].copy()
    df = df.nlargest(top_n, 'assists').sort_values('assists', ascending=True)
    
    df['label'] = df['player_name'] + ' (' + df['team'] + ')'
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['label'],
        x=df['assists'],
        orientation='h',
        marker_color=COLOR_PALETTE['secondary'],
        text=df['assists'],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Passes décisives: %{x}<extra></extra>'
    ))
    
    fig = apply_custom_theme(fig, f'Top {top_n} Passeurs')
    fig.update_layout(
        xaxis_title='Nombre de Passes Décisives',
        yaxis_title='Joueur',
        height=max(400, top_n * 30)
    )
    
    return fig


# ============ DISTRIBUTION CHARTS ============

def plot_age_distribution(teams_df):
    """Histogram of player age distribution"""
    from scraper import get_team_squad
    
    all_ages = []
    for _, team in teams_df.iterrows():
        squad = get_team_squad(team['team_name'])
        all_ages.extend(squad['age'].tolist())
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=all_ages,
        nbinsx=20,
        marker_color=COLOR_PALETTE['primary'],
        opacity=0.7,
        hovertemplate='Âge: %{x}<br>Nombre: %{y}<extra></extra>'
    ))
    
    fig = apply_custom_theme(fig, 'Distribution des Âges des Joueurs')
    fig.update_layout(
        xaxis_title='Âge',
        yaxis_title='Nombre de Joueurs',
        bargap=0.1
    )
    
    return fig


def plot_value_distribution(teams_df):
    """Histogram of player market value distribution"""
    from scraper import get_team_squad
    
    all_values = []
    for _, team in teams_df.iterrows():
        squad = get_team_squad(team['team_name'])
        all_values.extend(squad['market_value'].tolist())
    
    # Convert to millions for better readability
    all_values_m = [v / 1_000_000 for v in all_values if v > 0]
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=all_values_m,
        nbinsx=30,
        marker_color=COLOR_PALETTE['accent'],
        opacity=0.7,
        hovertemplate='Valeur: €%{x:.1f}M<br>Nombre: %{y}<extra></extra>'
    ))
    
    fig = apply_custom_theme(fig, 'Distribution des Valeurs Marchandes')
    fig.update_layout(
        xaxis_title='Valeur Marchande (Millions €)',
        yaxis_title='Nombre de Joueurs',
        bargap=0.1
    )
    
    return fig


# ============ PIE CHARTS ============

def plot_league_distribution(teams_df):
    """Pie chart of players by league/club"""
    from scraper import get_team_squad
    
    league_counts = {}
    for _, team in teams_df.iterrows():
        squad = get_team_squad(team['team_name'])
        for club in squad['club']:
            league_counts[club] = league_counts.get(club, 0) + 1
    
    # Group smaller leagues into "Other"
    sorted_leagues = sorted(league_counts.items(), key=lambda x: x[1], reverse=True)
    top_leagues = dict(sorted_leagues[:5])
    other_count = sum(count for _, count in sorted_leagues[5:])
    if other_count > 0:
        top_leagues['Other'] = other_count
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=list(top_leagues.keys()),
        values=list(top_leagues.values()),
        marker_colors=COLORS,
        hovertemplate='<b>%{label}</b><br>Joueurs: %{value}<br>%{percent}<extra></extra>'
    ))
    
    fig = apply_custom_theme(fig, 'Répartition des Joueurs par Championnat')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig


def plot_position_distribution(player_stats_df):
    """Pie chart of players by position"""
    position_counts = player_stats_df['position'].value_counts()
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=position_counts.index,
        values=position_counts.values,
        marker_colors=COLORS[:len(position_counts)],
        hovertemplate='<b>%{label}</b><br>Joueurs: %{value}<br>%{percent}<extra></extra>'
    ))
    
    fig = apply_custom_theme(fig, 'Répartition des Joueurs par Poste')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig


# ============ BOX PLOTS ============

def plot_value_boxplot(teams_df):
    """Box plot of value distribution by team"""
    from scraper import get_team_squad
    
    data = []
    for _, team in teams_df.iterrows():
        squad = get_team_squad(team['team_name'])
        for _, player in squad.iterrows():
            data.append({
                'team': team['team_name'],
                'value': player['market_value'] / 1_000_000
            })
    
    df = pd.DataFrame(data)
    
    fig = px.box(
        df,
        x='team',
        y='value',
        color='team',
        color_discrete_sequence=COLORS
    )
    
    fig = apply_custom_theme(fig, 'Distribution des Valeurs par Équipe')
    fig.update_layout(
        xaxis_title='Équipe',
        yaxis_title='Valeur Marchande (Millions €)',
        showlegend=False,
        height=500
    )
    fig.update_xaxes(tickangle=45)
    
    return fig


# ============ SCATTER PLOTS ============

def plot_value_vs_performance(team_stats_df):
    """Scatter plot of squad value vs goals scored"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=team_stats_df['squad_value'] / 1_000_000,
        y=team_stats_df['goals_scored'],
        mode='markers+text',
        marker=dict(
            size=12,
            color=team_stats_df['points'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Points')
        ),
        text=team_stats_df['team_name'],
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>Valeur: €%{x:.1f}M<br>Buts: %{y}<extra></extra>'
    ))
    
    fig = apply_custom_theme(fig, 'Valeur de l\'Équipe vs Performance')
    fig.update_layout(
        xaxis_title='Valeur de l\'Équipe (Millions €)',
        yaxis_title='Buts Marqués',
        height=600
    )
    
    return fig


def plot_age_vs_value(teams_df):
    """Scatter plot of average age vs team value"""
    from scraper import get_team_squad
    
    data = []
    for _, team in teams_df.iterrows():
        squad = get_team_squad(team['team_name'])
        data.append({
            'team': team['team_name'],
            'avg_age': squad['age'].mean(),
            'squad_value': team['squad_value'] / 1_000_000
        })
    
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['avg_age'],
        y=df['squad_value'],
        mode='markers+text',
        marker=dict(size=12, color=COLOR_PALETTE['secondary']),
        text=df['team'],
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>Âge moyen: %{x:.1f}<br>Valeur: €%{y:.1f}M<extra></extra>'
    ))
    
    fig = apply_custom_theme(fig, 'Âge Moyen vs Valeur de l\'Équipe')
    fig.update_layout(
        xaxis_title='Âge Moyen de l\'Équipe',
        yaxis_title='Valeur de l\'Équipe (Millions €)',
        height=600
    )
    
    return fig


# ============ HEATMAPS ============

def plot_correlation_heatmap(team_stats_df):
    """Correlation heatmap of team statistics"""
    # Select numeric columns
    numeric_cols = ['squad_value', 'goals_scored', 'goals_conceded', 
                    'avg_age', 'wins', 'points']
    
    corr_data = team_stats_df[numeric_cols].corr()
    
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        z=corr_data.values,
        x=['Valeur', 'Buts pour', 'Buts contre', 'Âge moy.', 'Victoires', 'Points'],
        y=['Valeur', 'Buts pour', 'Buts contre', 'Âge moy.', 'Victoires', 'Points'],
        colorscale='RdBu',
        zmid=0,
        text=corr_data.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        hovertemplate='%{x} vs %{y}<br>Corrélation: %{z:.2f}<extra></extra>'
    ))
    
    fig = apply_custom_theme(fig, 'Matrice de Corrélation des Statistiques')
    fig.update_layout(height=600)
    
    return fig


# ============ RADAR CHARTS ============

def plot_team_radar(team_stats_df, team_names):
    """Radar chart comparing team profiles"""
    if not team_names:
        team_names = team_stats_df['team_name'].head(3).tolist()
    
    fig = go.Figure()
    
    categories = ['Valeur', 'Buts', 'Défense', 'Points', 'Victoires']
    
    for team_name in team_names:
        team = team_stats_df[team_stats_df['team_name'] == team_name].iloc[0]
        
        # Normalize values to 0-100 scale
        max_value = team_stats_df['squad_value'].max()
        max_goals = team_stats_df['goals_scored'].max()
        max_defense = team_stats_df['goals_conceded'].min() or 1
        max_points = team_stats_df['points'].max()
        max_wins = team_stats_df['wins'].max()
        
        values = [
            (team['squad_value'] / max_value) * 100 if max_value > 0 else 0,
            (team['goals_scored'] / max_goals) * 100 if max_goals > 0 else 0,
            100 - ((team['goals_conceded'] / max_defense) * 100) if max_defense > 0 else 0,
            (team['points'] / max_points) * 100 if max_points > 0 else 0,
            (team['wins'] / max_wins) * 100 if max_wins > 0 else 0
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=team_name
        ))
    
    fig = apply_custom_theme(fig, 'Comparaison des Profils d\'Équipes')
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        height=600
    )
    
    return fig


# ============ LINE CHARTS ============

def plot_performance_evolution(matches_df, team_name):
    """Line chart showing team performance over matches"""
    team_matches = matches_df[
        (matches_df['team_home'] == team_name) | 
        (matches_df['team_away'] == team_name)
    ].copy()
    
    team_matches = team_matches.sort_values('date')
    
    cumulative_goals = []
    cumulative_points = []
    match_numbers = []
    
    total_goals = 0
    total_points = 0
    
    for idx, (_, match) in enumerate(team_matches.iterrows(), 1):
        # Skip matches that haven't been played yet (None scores)
        if pd.isna(match['score_home']) or pd.isna(match['score_away']):
            continue
            
        if match['team_home'] == team_name:
            goals = match['score_home']
            if match['score_home'] > match['score_away']:
                points = 3
            elif match['score_home'] == match['score_away']:
                points = 1
            else:
                points = 0
        else:
            goals = match['score_away']
            if match['score_away'] > match['score_home']:
                points = 3
            elif match['score_away'] == match['score_home']:
                points = 1
            else:
                points = 0
        
        total_goals += goals
        total_points += points
        
        cumulative_goals.append(total_goals)
        cumulative_points.append(total_points)
        match_numbers.append(idx)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=match_numbers,
            y=cumulative_goals,
            name='Buts Cumulés',
            line=dict(color=COLOR_PALETTE['primary'], width=3)
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=match_numbers,
            y=cumulative_points,
            name='Points Cumulés',
            line=dict(color=COLOR_PALETTE['secondary'], width=3)
        ),
        secondary_y=True
    )
    
    fig = apply_custom_theme(fig, f'Évolution des Performances - {team_name}')
    fig.update_xaxes(title_text='Numéro de Match')
    fig.update_yaxes(title_text='Buts Cumulés', secondary_y=False)
    fig.update_yaxes(title_text='Points Cumulés', secondary_y=True)
    fig.update_layout(height=500)
    
    return fig


# ============ GROUP COMPARISONS ============

def plot_group_comparison(team_stats_df):
    """Bar chart comparing groups"""
    group_stats = team_stats_df.groupby('group').agg({
        'squad_value': 'mean',
        'goals_scored': 'sum',
        'avg_age': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Valeur Moyenne', 'Total Buts', 'Âge Moyen')
    )
    
    fig.add_trace(
        go.Bar(
            x=group_stats['group'],
            y=group_stats['squad_value'] / 1_000_000,
            marker_color=COLOR_PALETTE['primary'],
            name='Valeur'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=group_stats['group'],
            y=group_stats['goals_scored'],
            marker_color=COLOR_PALETTE['success'],
            name='Buts'
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(
            x=group_stats['group'],
            y=group_stats['avg_age'],
            marker_color=COLOR_PALETTE['secondary'],
            name='Âge'
        ),
        row=1, col=3
    )
    
    fig = apply_custom_theme(fig, 'Comparaison des Groupes')
    fig.update_layout(height=400, showlegend=False)
    fig.update_yaxes(title_text='Millions €', row=1, col=1)
    fig.update_yaxes(title_text='Buts', row=1, col=2)
    fig.update_yaxes(title_text='Années', row=1, col=3)
    
    return fig
