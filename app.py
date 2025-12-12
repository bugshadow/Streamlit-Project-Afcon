"""
AFCON Analytics Dashboard
Professional Streamlit application for analyzing Africa Cup of Nations data

Author: Advanced Analytics Team
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

import scraper
import visualizations as viz


st.set_page_config(
    page_title="AFCON Analytics Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* BEAUTIFUL DARK THEME WITH VIBRANT COLORS */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 50%, #0f1419 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main content background */
    .main {
        background-color: transparent;
    }
    
    /* Main title styling - Vibrant gradient */
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00F260 0%, #0575E6 50%, #F7B801 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 242, 96, 0.3);
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #00F260;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Metric cards - Vibrant and modern */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        color: white;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar - Elegant gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d3a 0%, #0a0e27 100%);
        border-right: 2px solid rgba(0, 242, 96, 0.3);
    }
    
    /* Force all sidebar text to be white */
    [data-testid="stSidebar"] * {
        color: white !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Sidebar radio buttons - Beautiful hover effects */
    [data-testid="stSidebar"] .row-widget.stRadio > div {
        background-color: transparent;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio label {
        color: white !important;
        background: rgba(0, 242, 96, 0.1);
        padding: 0.9rem 1.2rem;
        border-radius: 12px;
        margin-bottom: 0.6rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(0, 242, 96, 0.2);
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio label:hover {
        background: linear-gradient(135deg, rgba(0, 242, 96, 0.3), rgba(5, 117, 230, 0.3));
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 4px 15px rgba(0, 242, 96, 0.4);
        border-color: #00F260;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio label[data-baseweb="radio"] > div:first-child {
        background-color: #00F260;
    }
    
    /* Sidebar titles */
    [data-testid="stSidebar"] h1 {
        color: white !important;
        text-shadow: 0 0 20px rgba(0, 242, 96, 0.5);
    }
    
    /* Button styling - Vibrant */
    .stButton>button {
        background: linear-gradient(135deg, #00F260 0%, #0575E6 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 242, 96, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 242, 96, 0.5);
        background: linear-gradient(135deg, #0575E6 0%, #00F260 100%);
    }
    
    /* ALL TEXT IN WHITE */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: white !important;
        font-weight: 600;
    }
    
    .main p, .main span, .main div, .main label {
        color: white !important;
    }
    
    /* Subheaders with gradient accent */
    h2, h3 {
        background: linear-gradient(135deg, #00F260, #0575E6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Markdown containers */
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: white !important;
    }
    
    .element-container p {
        color: white !important;
    }
    
    /* Tabs - Modern and vibrant */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        background: rgba(255, 255, 255, 0.05);
        color: white;
        border-radius: 10px;
        padding: 0 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 242, 96, 0.2);
        border-color: #00F260;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00F260, #0575E6);
        color: white !important;
        border-color: transparent;
        box-shadow: 0 4px 15px rgba(0, 242, 96, 0.4);
    }
    
    /* Expanders - Elegant */
    .streamlit-expanderHeader {
        color: white !important;
        background: rgba(0, 242, 96, 0.1);
        border-radius: 8px;
        border: 1px solid rgba(0, 242, 96, 0.3);
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(0, 242, 96, 0.2);
        border-color: #00F260;
    }
    
    /* Dataframes - Dark with borders */
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(0, 242, 96, 0.2);
    }
    
    /* Metrics - Vibrant cards */
    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #00F260 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #0575E6 !important;
    }
    
    /* Select boxes and inputs */
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: #00F260 !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(0, 242, 96, 0.3);
        color: white;
    }
    
    /* Dividers */
    hr {
        border-color: rgba(0, 242, 96, 0.3);
    }
    
    /* Info boxes */
    .stAlert {
        background-color: rgba(5, 117, 230, 0.2);
        border-left: 4px solid #0575E6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============ DATA LOADING ============

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    """Load all AFCON data with caching"""
    with st.spinner('Chargement des données AFCON...'):
        return scraper.load_all_data()

# Load data
try:
    data = load_data()
    teams_df = data['teams']
    player_stats_df = data['player_stats']
    matches_df = data['matches']
    team_stats_df = data['team_stats']
except Exception as e:
    st.error(f"Erreur lors du chargement des données: {e}")
    st.stop()

# ============ SIDEBAR NAVIGATION ============

st.sidebar.markdown("<h1 style='color: white; text-align: center;'>🏆 AFCON</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #F7B801; text-align: center; font-size: 0.9rem;'>Analytics Dashboard</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏆 Overview CAN", "🏅 Champions Historiques", "👥 Groupes & Classements", "⚽ Matchs & Résultats", 
     "🌟 Top Players", "📊 Analyses Comparatives"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<p style='color: white; font-size: 0.8rem;'>Dernière mise à jour:<br>{datetime.now().strftime('%d/%m/%Y %H:%M')}</p>", unsafe_allow_html=True)

# ============ PAGE 1: OVERVIEW CAN ============

if page == "🏆 Overview CAN":
    # Header
    st.markdown("<div class='main-title'>🏆 Coupe d'Afrique des Nations</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Vue d'ensemble et statistiques globales</div>", unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Équipes Participantes",
            value=len(teams_df),
            delta=f"{len(teams_df['group'].unique())} groupes"
        )
    
    with col2:
        total_players = len(player_stats_df)
        st.metric(
            label="Joueurs Totaux",
            value=total_players,
            delta=f"~{int(total_players/len(teams_df))} par équipe"
        )
    
    with col3:
        total_value = teams_df['squad_value'].sum() / 1_000_000
        st.metric(
            label="Valeur Totale",
            value=f"€{total_value:.0f}M",
            delta=f"€{teams_df['squad_value'].mean()/1_000_000:.0f}M moy."
        )
    
    with col4:
        total_goals = team_stats_df['goals_scored'].sum()
        st.metric(
            label="Buts Marqués",
            value=total_goals,
            delta=f"{total_goals/len(matches_df):.1f} par match"
        )
    
    st.markdown("---")
    
    # Top teams
    st.subheader("🏅 Top 3 Équipes par Valeur")
    top_3_teams = teams_df.nlargest(3, 'squad_value')
    
    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]
    
    for idx, (col, (_, team)) in enumerate(zip(cols, top_3_teams.iterrows())):
        with col:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FF6B35 0%, #F7B801 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center; color: white;'>
                <h1>{medals[idx]}</h1>
                <h3>{team['team_name']}</h3>
                <p style='font-size: 1.5rem; font-weight: bold;'>€{team['squad_value']/1_000_000:.1f}M</p>
                <p>{team['group']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(viz.plot_team_values(team_stats_df, top_n=10), use_container_width=True)
    
    with col2:
        st.plotly_chart(viz.plot_group_comparison(team_stats_df), use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(viz.plot_age_distribution(teams_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(viz.plot_value_distribution(teams_df), use_container_width=True)

# ============ PAGE 2: CHAMPIONS HISTORIQUES ============

elif page == "🏅 Champions Historiques":
    st.markdown("<div class='main-title'>🏆 CHAMPIONS HISTORIQUES CAN</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>67 Ans de Légende Africaine • 1957-2024</div>", unsafe_allow_html=True)
    
    # Country flags mapping
    country_flags = {
        'Egypt': '🇪🇬', 'Cameroon': '🇨🇲', 'Ghana': '🇬🇭', 'Nigeria': '🇳🇬',
        'Côte d\'Ivoire': '🇨🇮', 'Algeria': '🇩🇿', 'Senegal': '🇸🇳', 'Morocco': '🇲🇦',
        'Tunisia': '🇹🇳', 'South Africa': '🇿🇦', 'DR Congo': '🇨🇩', 'Zaire (DR Congo)': '🇨🇩',
        'Congo': '🇨🇬', 'Sudan': '🇸🇩', 'Ethiopia': '🇪🇹', 'Zambia': '🇿🇲',
        'Burkina Faso': '🇧🇫', 'Guinea': '🇬🇳', 'Mali': '🇲🇱', 'Gabon': '🇬🇦',
        'Equatorial Guinea': '🇬🇶', 'Angola': '🇦🇴', 'Uganda': '🇺🇬', 'Libya': '🇱🇾'
    }
    
    champions_data = [
        {'year': 2024, 'host': 'Côte d\'Ivoire', 'champion': 'Côte d\'Ivoire', 'runner_up': 'Nigeria', 'score': '2-1'},
        {'year': 2023, 'host': 'Côte d\'Ivoire (rep.)', 'champion': 'Senegal', 'runner_up': 'Egypt', 'score': '0-0 (4-2 pen)'},
        {'year': 2021, 'host': 'Cameroon', 'champion': 'Senegal', 'runner_up': 'Egypt', 'score': '0-0 (4-2 pen)'},
        {'year': 2019, 'host': 'Egypt', 'champion': 'Algeria', 'runner_up': 'Senegal', 'score': '1-0'},
        {'year': 2017, 'host': 'Gabon', 'champion': 'Cameroon', 'runner_up': 'Egypt', 'score': '2-1'},
        {'year': 2015, 'host': 'Equatorial Guinea', 'champion': 'Côte d\'Ivoire', 'runner_up': 'Ghana', 'score': '0-0 (9-8 pen)'},
        {'year': 2013, 'host': 'South Africa', 'champion': 'Nigeria', 'runner_up': 'Burkina Faso', 'score': '1-0'},
        {'year': 2012, 'host': 'Gabon/Eq. Guinea', 'champion': 'Zambia', 'runner_up': 'Côte d\'Ivoire', 'score': '0-0 (8-7 pen)'},
        {'year': 2010, 'host': 'Angola', 'champion': 'Egypt', 'runner_up': 'Ghana', 'score': '1-0'},
        {'year': 2008, 'host': 'Ghana', 'champion': 'Egypt', 'runner_up': 'Cameroon', 'score': '1-0'},
        {'year': 2006, 'host': 'Egypt', 'champion': 'Egypt', 'runner_up': 'Côte d\'Ivoire', 'score': '0-0 (4-2 pen)'},
        {'year': 2004, 'host': 'Tunisia', 'champion': 'Tunisia', 'runner_up': 'Morocco', 'score': '2-1'},
        {'year': 2002, 'host': 'Mali', 'champion': 'Cameroon', 'runner_up': 'Senegal', 'score': '0-0 (3-2 pen)'},
        {'year': 2000, 'host': 'Ghana/Nigeria', 'champion': 'Cameroon', 'runner_up': 'Nigeria', 'score': '2-2 (4-3 pen)'},
        {'year': 1998, 'host': 'Burkina Faso', 'champion': 'Egypt', 'runner_up': 'South Africa', 'score': '2-0'},
        {'year': 1996, 'host': 'South Africa', 'champion': 'South Africa', 'runner_up': 'Tunisia', 'score': '2-0'},
        {'year': 1994, 'host': 'Tunisia', 'champion': 'Nigeria', 'runner_up': 'Zambia', 'score': '2-1'},
        {'year': 1992, 'host': 'Senegal', 'champion': 'Côte d\'Ivoire', 'runner_up': 'Ghana', 'score': '0-0 (11-10 pen)'},
        {'year': 1990, 'host': 'Algeria', 'champion': 'Algeria', 'runner_up': 'Nigeria', 'score': '1-0'},
        {'year': 1988, 'host': 'Morocco', 'champion': 'Cameroon', 'runner_up': 'Nigeria', 'score': '1-0'},
        {'year': 1986, 'host': 'Egypt', 'champion': 'Egypt', 'runner_up': 'Cameroon', 'score': '0-0 (5-4 pen)'},
        {'year': 1984, 'host': 'Côte d\'Ivoire', 'champion': 'Cameroon', 'runner_up': 'Nigeria', 'score': '3-1'},
        {'year': 1982, 'host': 'Libya', 'champion': 'Ghana', 'runner_up': 'Libya', 'score': '1-1 (7-6 pen)'},
        {'year': 1980, 'host': 'Nigeria', 'champion': 'Nigeria', 'runner_up': 'Algeria', 'score': '3-0'},
        {'year': 1978, 'host': 'Ghana', 'champion': 'Ghana', 'runner_up': 'Uganda', 'score': '2-0'},
        {'year': 1976, 'host': 'Ethiopia', 'champion': 'Morocco', 'runner_up': 'Guinea', 'score': '1-1'},
        {'year': 1974, 'host': 'Egypt', 'champion': 'Zaire (DR Congo)', 'runner_up': 'Zambia', 'score': '2-2'},
        {'year': 1972, 'host': 'Cameroon', 'champion': 'Congo', 'runner_up': 'Mali', 'score': '3-2'},
        {'year': 1970, 'host': 'Sudan', 'champion': 'Sudan', 'runner_up': 'Ghana', 'score': '1-0'},
        {'year': 1968, 'host': 'Ethiopia', 'champion': 'Zaire (DR Congo)', 'runner_up': 'Ghana', 'score': '1-0'},
        {'year': 1965, 'host': 'Tunisia', 'champion': 'Ghana', 'runner_up': 'Tunisia', 'score': '3-2'},
        {'year': 1963, 'host': 'Ghana', 'champion': 'Ghana', 'runner_up': 'Sudan', 'score': '3-0'},
        {'year': 1962, 'host': 'Ethiopia', 'champion': 'Ethiopia', 'runner_up': 'Egypt', 'score': '4-2'},
        {'year': 1959, 'host': 'Egypt', 'champion': 'Egypt', 'runner_up': 'Sudan', 'score': '2-1'},
        {'year': 1957, 'host': 'Sudan', 'champion': 'Egypt', 'runner_up': 'Ethiopia', 'score': '4-0'},
    ]
    
    champions_df = pd.DataFrame(champions_data)
    title_counts = champions_df['champion'].value_counts()
    
    # ========== PODIUM SECTION - TOP 3 ==========
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🥇 PODIUM DES LÉGENDES")
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    # 2nd Place - Silver
    with col1:
        country_2 = title_counts.index[1]
        titles_2 = title_counts.iloc[1]
        flag_2 = country_flags.get(country_2, '🏴')
        st.markdown(f"""
        <div style='
            background: linear-gradient(145deg, #E8E8E8 0%, #B8B8B8 100%);
            padding: 2rem 1rem;
            border-radius: 20px;
            text-align: center;
            margin-top: 3rem;
            box-shadow: 0 15px 40px rgba(184, 184, 184, 0.5), 
                        inset 0 -5px 20px rgba(255,255,255,0.3);
            border: 3px solid #C0C0C0;
            position: relative;
            overflow: hidden;
            transform: perspective(1000px) rotateY(-5deg);'>
            <div style='position: absolute; top: -30px; right: -30px; font-size: 120px; opacity: 0.15;'>🥈</div>
            <div style='font-size: 5rem; margin: 0;'>{flag_2}</div>
            <h2 style='color: #424242; font-weight: 900; margin: 0.5rem 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
                {country_2}
            </h2>
            <div style='background: rgba(255,255,255,0.4); padding: 0.8rem; border-radius: 12px; margin: 1rem 0;'>
                <div style='font-size: 3.5rem; font-weight: 900; color: #2c3e50; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);'>
                    {titles_2}
                </div>
                <div style='font-size: 1rem; color: #555; font-weight: 600;'>TITRES</div>
            </div>
            <div style='font-size: 4rem; margin-top: 0.5rem;'>🥈</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 1st Place - Gold (Center, Larger)
    with col2:
        country_1 = title_counts.index[0]
        titles_1 = title_counts.iloc[0]
        flag_1 = country_flags.get(country_1, '🏴')
        st.markdown(f"""
        <div style='
            background: linear-gradient(145deg, #FFD700 0%, #FFA500 100%);
            padding: 2.5rem 1rem;
            border-radius: 25px;
            text-align: center;
            margin-top: 0;
            box-shadow: 0 20px 60px rgba(255, 215, 0, 0.6), 
                        inset 0 -8px 25px rgba(255,255,255,0.4),
                        0 0 80px rgba(255, 215, 0, 0.4);
            border: 4px solid #FFD700;
            position: relative;
            overflow: hidden;
            transform: scale(1.05);
            animation: pulse 2s infinite;'>
            <div style='position: absolute; top: -40px; right: -40px; font-size: 150px; opacity: 0.15;'>🥇</div>
            <div style='font-size: 6rem; margin: 0; filter: drop-shadow(0 5px 10px rgba(0,0,0,0.3));'>{flag_1}</div>
            <h1 style='color: #5D4E00; font-weight: 900; margin: 0.8rem 0; font-size: 1.8rem; text-shadow: 3px 3px 6px rgba(0,0,0,0.3);'>
                {country_1}
            </h1>
            <div style='background: rgba(255,255,255,0.5); padding: 1rem; border-radius: 15px; margin: 1rem 0;'>
                <div style='font-size: 4.5rem; font-weight: 900; color: #8B4500; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
                    {titles_1}
                </div>
                <div style='font-size: 1.1rem; color: #5D4E00; font-weight: 700; letter-spacing: 2px;'>TITRES</div>
            </div>
            <div style='font-size: 5rem; margin-top: 1rem; animation: bounce 1s infinite;'>👑</div>
        </div>
        <style>
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1.05); }}
                50% {{ transform: scale(1.08); }}
            }}
            @keyframes bounce {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-10px); }}
            }}
        </style>
        """, unsafe_allow_html=True)
    
    # 3rd Place - Bronze
    with col3:
        country_3 = title_counts.index[2]
        titles_3 = title_counts.iloc[2]
        flag_3 = country_flags.get(country_3, '🏴')
        st.markdown(f"""
        <div style='
            background: linear-gradient(145deg, #CD7F32 0%, #8B4513 100%);
            padding: 2rem 1rem;
            border-radius: 20px;
            text-align: center;
            margin-top: 3rem;
            box-shadow: 0 15px 40px rgba(205, 127, 50, 0.5), 
                        inset 0 -5px 20px rgba(255,255,255,0.2);
            border: 3px solid #B87333;
            position: relative;
            overflow: hidden;
            transform: perspective(1000px) rotateY(5deg);'>
            <div style='position: absolute; top: -30px; left: -30px; font-size: 120px; opacity: 0.15;'>🥉</div>
            <div style='font-size: 5rem; margin: 0;'>{flag_3}</div>
            <h2 style='color: #FFF; font-weight: 900; margin: 0.5rem 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                {country_3}
            </h2>
            <div style='background: rgba(255,255,255,0.3); padding: 0.8rem; border-radius: 12px; margin: 1rem 0;'>
                <div style='font-size: 3.5rem; font-weight: 900; color: #FFF; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>
                    {titles_3}
                </div>
                <div style='font-size: 1rem; color: #FFE4B5; font-weight: 600;'>TITRES</div>
            </div>
            <div style='font-size: 4rem; margin-top: 0.5rem;'>🥉</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ========== OTHER WINNERS - Modern Cards Grid ==========
    st.markdown("### 🏅 HALL OF FAME")
    
    other_winners = title_counts.iloc[3:12]
    
    # Create grid of 3 columns
    for i in range(0, len(other_winners), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(other_winners):
                country = other_winners.index[idx]
                titles = other_winners.iloc[idx]
                flag = country_flags.get(country, '🏴')
                rank = idx + 4
                
                with col:
                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, rgba(0, 242, 96, 0.15) 0%, rgba(5, 117, 230, 0.15) 100%);
                        backdrop-filter: blur(10px);
                        padding: 1.5rem;
                        border-radius: 18px;
                        text-align: center;
                        margin-bottom: 1rem;
                        border: 2px solid rgba(0, 242, 96, 0.3);
                        box-shadow: 0 8px 32px rgba(0, 242, 96, 0.2);
                        transition: all 0.3s ease;
                        cursor: pointer;'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                            <span style='background: rgba(0, 242, 96, 0.3); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.9rem; font-weight: 700;'>
                                #{rank}
                            </span>
                            <span style='font-size: 2rem;'>🏅</span>
                        </div>
                        <div style='font-size: 4rem; margin: 0.5rem 0;'>{flag}</div>
                        <h3 style='color: white; font-weight: 700; margin: 0.5rem 0; font-size: 1.2rem;'>{country}</h3>
                        <div style='background: linear-gradient(135deg, #00F260, #0575E6); 
                                    padding: 0.8rem; border-radius: 12px; margin-top: 1rem;'>
                            <div style='font-size: 2.5rem; font-weight: 900; color: white;'>{titles}</div>
                            <div style='font-size: 0.85rem; color: rgba(255,255,255,0.9); font-weight: 600;'>
                                {'TITRE' if titles == 1 else 'TITRES'}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========== STATS SECTION ==========
    st.markdown("### 📊 STATISTIQUES")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_editions = len(champions_df)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem 1rem; border-radius: 15px; text-align: center;
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);'>
            <div style='font-size: 3rem;'>📅</div>
            <div style='font-size: 2.5rem; font-weight: 900; color: white; margin: 0.5rem 0;'>{total_editions}</div>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.95rem; font-weight: 600;'>ÉDITIONS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_champions = len(title_counts)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 2rem 1rem; border-radius: 15px; text-align: center;
                    box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4);'>
            <div style='font-size: 3rem;'>🌍</div>
            <div style='font-size: 2.5rem; font-weight: 900; color: white; margin: 0.5rem 0;'>{total_champions}</div>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.95rem; font-weight: 600;'>PAYS CHAMPIONS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        home_wins = len(champions_df[champions_df['champion'] == champions_df['host']])
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 2rem 1rem; border-radius: 15px; text-align: center;
                    box-shadow: 0 10px 30px rgba(0, 242, 254, 0.4);'>
            <div style='font-size: 3rem;'>🏠</div>
            <div style='font-size: 2.5rem; font-weight: 900; color: white; margin: 0.5rem 0;'>{home_wins}</div>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.95rem; font-weight: 600;'>VICTOIRES À DOMICILE</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        first_year = champions_df['year'].min()
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                    padding: 2rem 1rem; border-radius: 15px; text-align: center;
                    box-shadow: 0 10px 30px rgba(250, 112, 154, 0.4);'>
            <div style='font-size: 3rem;'>⏳</div>
            <div style='font-size: 2.5rem; font-weight: 900; color: white; margin: 0.5rem 0;'>{first_year}</div>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.95rem; font-weight: 600;'>PREMIÈRE ÉDITION</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========== TIMELINE TABLE ==========
    st.markdown("### 📜 CHRONOLOGIE COMPLÈTE")
    
    champions_display = champions_df.copy()
    champions_display['champion_display'] = champions_display['champion'].apply(
        lambda x: f"{country_flags.get(x, '🏴')} {x}"
    )
    champions_display['runner_up_display'] = champions_display['runner_up'].apply(
        lambda x: f"{country_flags.get(x, '🏴')} {x}"
    )
    
    champions_display = champions_display[['year', 'host', 'champion_display', 'runner_up_display', 'score']]
    champions_display.columns = ['Année', 'Pays hôte', '🏆 Champion', '🥈 Finaliste', 'Score']
    champions_display = champions_display.sort_values('Année', ascending=False)
    champions_display.index = range(1, len(champions_display) + 1)
    
    st.dataframe(
        champions_display, 
        use_container_width=True,
        height=500,
        column_config={
            'Année': st.column_config.NumberColumn(format="%d", width="small"),
            '🏆 Champion': st.column_config.TextColumn(width="medium"),
            '🥈 Finaliste': st.column_config.TextColumn(width="medium"),
        }
    )

# ============ PAGE 3: GROUPES & CLASSEMENTS ============

elif page == "👥 Groupes & Classements":
    st.markdown("<div class='main-title'>👥 Groupes & Classements</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Composition des groupes et classements détaillés</div>", unsafe_allow_html=True)
    
    # Group selector
    groups = sorted(teams_df['group'].unique())
    
    # Tabs for each group
    tabs = st.tabs(groups)
    
    for tab, group in zip(tabs, groups):
        with tab:
            st.subheader(f"Classement {group}")
            
            # Get group standings
            standings = scraper.get_group_standings(group)
            
            # Display standings table
            standings_display = standings[['team_name', 'matches_played', 'wins', 'draws', 
                                          'losses', 'goals_scored', 'goals_conceded', 
                                          'goal_difference', 'points']].copy()
            
            standings_display.columns = ['Équipe', 'MJ', 'V', 'N', 'D', 'BP', 'BC', 'Diff', 'Pts']
            standings_display.index = range(1, len(standings_display) + 1)
            
            st.dataframe(
                standings_display,
                use_container_width=True,
                height=200
            )
            
            # Group statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_value = standings['squad_value'].sum() / 1_000_000
                st.metric("Valeur Totale du Groupe", f"€{total_value:.0f}M")
            
            with col2:
                avg_age = standings['avg_age'].mean()
                st.metric("Âge Moyen du Groupe", f"{avg_age:.1f} ans")
            
            with col3:
                total_goals = standings['goals_scored'].sum()
                st.metric("Buts Marqués", total_goals)
            
            # Visualizations for this group
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = viz.plot_team_values(standings, top_n=None)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = viz.plot_goals_by_team(standings)
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Overall group comparison
    st.subheader("📊 Comparaison entre Groupes")
    st.plotly_chart(viz.plot_group_comparison(team_stats_df), use_container_width=True)

# ============ PAGE 3: MATCHS & RÉSULTATS ============

elif page == "⚽ Matchs & Résultats":
    st.markdown("<div class='main-title'>⚽ Matchs & Résultats</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Calendrier complet de la CAN 2025 au Maroc</div>", unsafe_allow_html=True)
    
    # Phase filter
    phases = ['Tous'] + sorted(matches_df['phase'].unique().tolist())
    selected_phase = st.selectbox("Filtrer par phase", phases)
    
    # Filter matches
    if selected_phase != 'Tous':
        filtered_matches = matches_df[matches_df['phase'] == selected_phase]
    else:
        filtered_matches = matches_df
    
    # Info banner
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #00F260, #0575E6); 
                padding: 1rem 1.5rem; 
                border-radius: 12px; 
                margin-bottom: 2rem;
                border-left: 5px solid #F7B801;'>
        <p style='color: white; margin: 0; font-size: 1.1rem; font-weight: 600;'>
            ⚡ <strong>{len(filtered_matches)}</strong> matchs programmés pour la CAN 2025 au Maroc
            <br><span style='font-size: 0.95rem; opacity: 0.9;'>
            🗓️ Coup d'envoi: 21 Décembre 2025 • 🏆 Finale: 18 Janvier 2026
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # If Group Stage is selected, organize by groups
    if selected_phase == 'Group Stage':
        groups = sorted(filtered_matches['group'].unique())
        
        for group in groups:
            st.markdown(f"### 🏟️ {group}")
            group_matches = filtered_matches[filtered_matches['group'] == group].sort_values('date')
            
            # Display matches for this group
            for idx, match in group_matches.iterrows():
                with st.container():
                    # Match card with custom styling
                    col1, col2, col3 = st.columns([2, 1, 2])
                    
                    with col1:
                        st.markdown(f"<h3 style='text-align: right; color: white; margin: 0;'>{match['team_home']}</h3>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div style='text-align: center;'>
                            <div style='background: linear-gradient(135deg, #00F260, #0575E6); 
                                        padding: 0.5rem 1rem; 
                                        border-radius: 8px; 
                                        font-weight: 700; 
                                        color: white;
                                        display: inline-block;'>
                                VS
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"<h3 style='text-align: left; color: white; margin: 0;'>{match['team_away']}</h3>", unsafe_allow_html=True)
                    
                    # Match info
                    col_date, col_status = st.columns(2)
                    with col_date:
                        st.markdown(f"📅 **{match['date']}**")
                    with col_status:
                        st.markdown(f"🔔 **<span style='color: #00F260;'>À venir</span>**", unsafe_allow_html=True)
                    
                    st.markdown("---")
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    else:
        # For other phases or "Tous", display all matches
        for _, match in filtered_matches.iterrows():
            # Skip TBD matches in display
            if match['team_home'] == 'TBD' or match['team_away'] == 'TBD':
                continue
            
            with st.container():
                # Match card
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    st.markdown(f"<h3 style='text-align: right; color: white; margin: 0;'>{match['team_home']}</h3>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style='text-align: center;'>
                        <div style='background: linear-gradient(135deg, #00F260, #0575E6); 
                                    padding: 0.5rem 1rem; 
                                    border-radius: 8px; 
                                    font-weight: 700; 
                                    color: white;
                                    display: inline-block;'>
                            VS
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"<h3 style='text-align: left; color: white; margin: 0;'>{match['team_away']}</h3>", unsafe_allow_html=True)
                
                # Match info
                col_date, col_phase, col_status = st.columns(3)
                with col_date:
                    st.markdown(f"📅 **{match['date']}**")
                with col_phase:
                    phase_emoji = "🏟️" if match['phase'] == 'Group Stage' else "🏆"
                    st.markdown(f"{phase_emoji} **{match['phase']}**")
                with col_status:
                    st.markdown(f"🔔 **<span style='color: #00F260;'>À venir</span>**", unsafe_allow_html=True)
                
                st.markdown("---")
    
    #Statistics - only if there are finished matches
    st.markdown("<br>", unsafe_allow_html=True)
    finished_matches = filtered_matches[filtered_matches['status'] == 'Finished']
    
    if len(finished_matches) > 0:
        st.subheader("📊 Statistiques des Matchs")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_goals = (finished_matches['score_home'].sum() + finished_matches['score_away'].sum()) / len(finished_matches)
            st.metric("Buts par Match", f"{avg_goals:.2f}")
        
        with col2:
            home_wins = len(finished_matches[finished_matches['score_home'] > finished_matches['score_away']])
            st.metric("Victoires à Domicile", f"{home_wins} ({100*home_wins/len(finished_matches):.0f}%)")
        
        with col3:
            draws = len(finished_matches[finished_matches['score_home'] == finished_matches['score_away']])
            st.metric("Matchs Nuls", f"{draws} ({100*draws/len(finished_matches):.0f}%)")
    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea, #764ba2);
                    padding: 2rem;
                    border-radius: 15px;
                    text-align: center;'>
            <h3 style='color: white; margin: 0;'>📊 Statistiques</h3>
            <p style='color: rgba(255,255,255,0.9); margin: 1rem 0 0 0;'>
                Les statistiques seront disponibles une fois que les matchs auront été joués!
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============ PAGE 4: TOP PLAYERS ============

elif page == "🌟 Top Players":
    st.markdown("<div class='main-title'>🌟 Top Players</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Classements des meilleurs joueurs du tournoi</div>", unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_position = st.selectbox(
            "Filtrer par poste",
            ['Tous'] + sorted(player_stats_df['position'].unique().tolist())
        )
    
    with col2:
        selected_team = st.selectbox(
            "Filtrer par équipe",
            ['Tous'] + sorted(teams_df['team_name'].tolist())
        )
    
    with col3:
        top_n = st.slider("Nombre de joueurs", 5, 30, 15)
    
    # Apply filters
    filtered_players = player_stats_df.copy()
    
    if selected_position != 'Tous':
        filtered_players = filtered_players[filtered_players['position'] == selected_position]
    
    if selected_team != 'Tous':
        filtered_players = filtered_players[filtered_players['team'] == selected_team]
    
    # Tabs for different rankings
    tab1, tab2, tab3, tab4 = st.tabs(["⚽ Buteurs", "🎯 Passeurs", "💎 Plus Chers", "📊 Statistiques"])
    
    with tab1:
        st.subheader("🥇 Meilleurs Buteurs")
        
        top_scorers = filtered_players[filtered_players['goals'] > 0].nlargest(top_n, 'goals')
        
        if len(top_scorers) > 0:
            # Display chart
            st.plotly_chart(viz.plot_top_scorers(filtered_players, top_n), use_container_width=True)
            
            # Detailed table
            scorers_table = top_scorers[['player_name', 'team', 'position', 'goals', 'assists', 'games_played']].copy()
            scorers_table.columns = ['Joueur', 'Équipe', 'Poste', 'Buts', 'Passes', 'Matchs']
            scorers_table.index = range(1, len(scorers_table) + 1)
            
            st.dataframe(scorers_table, use_container_width=True)
        else:
            st.info("Aucun buteur trouvé avec ces filtres")
    
    with tab2:
        st.subheader("🎯 Meilleurs Passeurs")
        
        top_assisters = filtered_players[filtered_players['assists'] > 0].nlargest(top_n, 'assists')
        
        if len(top_assisters) > 0:
            # Display chart
            st.plotly_chart(viz.plot_top_assists(filtered_players, top_n), use_container_width=True)
            
            # Detailed table
            assisters_table = top_assisters[['player_name', 'team', 'position', 'assists', 'goals', 'games_played']].copy()
            assisters_table.columns = ['Joueur', 'Équipe', 'Poste', 'Passes', 'Buts', 'Matchs']
            assisters_table.index = range(1, len(assisters_table) + 1)
            
            st.dataframe(assisters_table, use_container_width=True)
        else:
            st.info("Aucun passeur trouvé avec ces filtres")
    
    with tab3:
        st.subheader("💎 Joueurs les Plus Chers")
        
        # Get market values from squad data
        all_valuable_players = []
        for _, team in teams_df.iterrows():
            squad = scraper.get_team_squad(team['team_name'])
            for _, player in squad.iterrows():
                all_valuable_players.append({
                    'player_name': player['player_name'],
                    'team': team['team_name'],
                    'position': player['position'],
                    'age': player['age'],
                    'market_value': player['market_value']
                })
        
        valuable_df = pd.DataFrame(all_valuable_players)
        
        # Apply filters
        if selected_position != 'Tous':
            valuable_df = valuable_df[valuable_df['position'] == selected_position]
        if selected_team != 'Tous':
            valuable_df = valuable_df[valuable_df['team'] == selected_team]
        
        top_valuable = valuable_df.nlargest(top_n, 'market_value')
        
        # Table
        valuable_table = top_valuable[['player_name', 'team', 'position', 'age', 'market_value']].copy()
        valuable_table['market_value'] = valuable_table['market_value'].apply(lambda x: f"€{x/1_000_000:.1f}M")
        valuable_table.columns = ['Joueur', 'Équipe', 'Poste', 'Âge', 'Valeur']
        valuable_table.index = range(1, len(valuable_table) + 1)
        
        st.dataframe(valuable_table, use_container_width=True, height=600)
    
    with tab4:
        st.subheader("📊 Statistiques Générales")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(viz.plot_position_distribution(filtered_players), use_container_width=True)
        
        with col2:
            # Create a simple stats comparison
            stats_summary = {
                'Total Joueurs': len(filtered_players),
                'Buts Totaux': filtered_players['goals'].sum(),
                'Passes Totales': filtered_players['assists'].sum(),
                'Minutes Jouées': filtered_players['minutes_played'].sum(),
                'Cartons Jaunes': filtered_players['yellow_cards'].sum(),
                'Cartons Rouges': filtered_players['red_cards'].sum()
            }
            
            st.markdown("### 📈 Résumé")
            for key, value in stats_summary.items():
                st.metric(key, value)

# ============ PAGE 5: ANALYSES COMPARATIVES ============

elif page == "📊 Analyses Comparatives":
    st.markdown("<div class='main-title'>📊 Analyses Comparatives</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Comparaisons d'équipes et analyses statistiques</div>", unsafe_allow_html=True)
    
    # Team comparison
    st.subheader("🔄 Comparaison d'Équipes")
    
    selected_teams = st.multiselect(
        "Sélectionnez les équipes à comparer (max 4)",
        teams_df['team_name'].tolist(),
        default=teams_df.nlargest(3, 'squad_value')['team_name'].tolist()[:3],
        max_selections=4
    )
    
    if len(selected_teams) >= 2:
        # Radar chart comparison
        st.plotly_chart(viz.plot_team_radar(team_stats_df, selected_teams), use_container_width=True)
        
        # Side-by-side comparison
        st.subheader("📋 Comparaison Détaillée")
        
        comparison_data = team_stats_df[team_stats_df['team_name'].isin(selected_teams)].copy()
        comparison_data['squad_value'] = comparison_data['squad_value'].apply(lambda x: f"€{x/1_000_000:.0f}M")
        comparison_data['avg_age'] = comparison_data['avg_age'].apply(lambda x: f"{x:.1f}")
        
        comparison_display = comparison_data[[
            'team_name', 'squad_value', 'avg_age', 'matches_played', 
            'wins', 'draws', 'losses', 'goals_scored', 'goals_conceded', 'points'
        ]].T
        
        comparison_display.columns = comparison_data['team_name'].tolist()
        comparison_display.index = [
            'Équipe', 'Valeur', 'Âge Moy.', 'Matchs', 
            'Victoires', 'Nuls', 'Défaites', 'Buts Pour', 'Buts Contre', 'Points'
        ]
        
        st.dataframe(comparison_display, use_container_width=True)
        
        # Performance evolution
        st.subheader("📈 Évolution des Performances")
        
        selected_team_for_evolution = st.selectbox(
            "Choisir une équipe", 
            selected_teams
        )
        
        st.plotly_chart(
            viz.plot_performance_evolution(matches_df, selected_team_for_evolution),
            use_container_width=True
        )
    else:
        st.info("Veuillez sélectionner au moins 2 équipes pour la comparaison")
    
    st.markdown("---")
    
    # Statistical analyses
    st.subheader("🔬 Analyses Statistiques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(viz.plot_value_vs_performance(team_stats_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(viz.plot_age_vs_value(teams_df), use_container_width=True)
    
    # Correlation heatmap
    st.subheader("🔗 Matrice de Corrélation")
    st.plotly_chart(viz.plot_correlation_heatmap(team_stats_df), use_container_width=True)
    
    # Box plot
    st.subheader("📦 Distribution des Valeurs par Équipe")
    st.plotly_chart(viz.plot_value_boxplot(teams_df), use_container_width=True)

# ============ FOOTER ============

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 2rem;'>
    <p><strong>AFCON Analytics Dashboard</strong></p>
    <p>Données extraites de Transfermarkt | Développé avec ❤️ pour l'analyse de la CAN</p>
    <p style='font-size: 0.8rem;'>© 2024 - Tous droits réservés</p>
</div>
""", unsafe_allow_html=True)
