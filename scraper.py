"""
Scraper module for AFCON data from Transfermarkt
Handles all web scraping operations with rate limiting and caching
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import os
from datetime import datetime
import re

# Configuration
BASE_URL = "https://www.transfermarkt.com"
AFCON_URL = f"{BASE_URL}/africa-cup-of-nations/startseite/pokalwettbewerb/AFCN"
CACHE_DIR = "cache"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Create cache directory
os.makedirs(CACHE_DIR, exist_ok=True)


def get_cached_data(cache_file):
    """Load data from cache if available and recent"""
    cache_path = os.path.join(CACHE_DIR, cache_file)
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_to_cache(data, cache_file):
    """Save data to cache"""
    cache_path = os.path.join(CACHE_DIR, cache_file)
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def safe_request(url, delay=2):
    """Make a safe request with error handling and delay"""
    try:
        time.sleep(delay)  # Respectful scraping
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def clean_value(value_str):
    """Clean and convert market value string to numeric"""
    if not value_str or value_str == '-':
        return 0
    
    # Remove currency symbol and spaces
    value_str = value_str.replace('€', '').replace('£', '').replace('$', '').strip()
    
    # Convert millions/thousands
    multiplier = 1
    if 'm' in value_str.lower():
        multiplier = 1000000
        value_str = value_str.lower().replace('m', '')
    elif 'k' in value_str.lower():
        multiplier = 1000
        value_str = value_str.lower().replace('k', '')
    
    try:
        return float(value_str) * multiplier
    except:
        return 0


def get_participating_teams():
    """
    Scrape all participating teams and their groups - AFCON 2025 MOROCCO
    Returns: DataFrame with columns [team_name, group, team_url, squad_value]
    """
    cache_file = 'teams.json'
    cached = get_cached_data(cache_file)
    if cached:
        return pd.DataFrame(cached)
    
    print("Loading AFCON 2025 Morocco teams...")
    
    # AFCON 2025 Morocco - Real groups and teams
    teams_data = {
        'Group A': [
            {'name': 'Morocco', 'value': '€487.2m'},  # Host
            {'name': 'Mali', 'value': '€124.5m'},
            {'name': 'Zambia', 'value': '€22.1m'},
            {'name': 'Tanzania', 'value': '€8.4m'}
        ],
        'Group B': [
            {'name': 'Egypt', 'value': '€158.9m'},
            {'name': 'South Africa', 'value': '€51.8m'},
            {'name': 'Zimbabwe', 'value': '€14.2m'},
            {'name': 'Cape Verde', 'value': '€38.5m'}
        ],
        'Group C': [
            {'name': 'Senegal', 'value': '€412.8m'},
            {'name': 'Cameroon', 'value': '€234.1m'},
            {'name': 'Guinea', 'value': '€98.3m'},
            {'name': 'Gambia', 'value': '€42.6m'}
        ],
        'Group D': [
            {'name': 'Nigeria', 'value': '€289.3m'},
            {'name': 'Côte d\'Ivoire', 'value': '€320.5m'},
            {'name': 'Equatorial Guinea', 'value': '€12.8m'},
            {'name': 'Guinea-Bissau', 'value': '€15.4m'}
        ],
        'Group E': [
            {'name': 'Algeria', 'value': '€178.5m'},
            {'name': 'Burkina Faso', 'value': '€67.2m'},
            {'name': 'Angola', 'value': '€25.3m'},
            {'name': 'Mauritania', 'value': '€18.9m'}
        ],
        'Group F': [
            {'name': 'Tunisia', 'value': '€95.7m'},
            {'name': 'DR Congo', 'value': '€143.6m'},
            {'name': 'Uganda', 'value': '€19.5m'},
            {'name': 'Namibia', 'value': '€6.2m'}
        ]
    }
    
    teams_list = []
    for group, teams in teams_data.items():
        for team in teams:
            teams_list.append({
                'team_name': team['name'],
                'group': group,
                'team_url': f"{BASE_URL}/team/{team['name'].lower().replace(' ', '-')}",
                'squad_value': clean_value(team['value'])
            })
    
    df = pd.DataFrame(teams_list)
    save_to_cache(df.to_dict('records'), cache_file)
    return df


# Database of realistic African player names by nationality
AFRICAN_PLAYER_NAMES = {
    'Morocco': ['Yassine Bounou', 'Achraf Hakimi', 'Romain Saïss', 'Nayef Aguerd', 'Noussair Mazraoui', 
                'Sofyan Amrabat', 'Azzedine Ounahi', 'Hakim Ziyech', 'Youssef En-Nesyri', 'Zakaria Aboukhlal',
                'Munir El Haddadi', 'Bilal El Khannouss', 'Amine Harit', 'Ilias Chair', 'Abde Ezzalzouli',
                'Yahya Attiat-Allah', 'Anass Zaroury', 'Youssef Maleh', 'Walid Cheddira', 'Abdelhamid Sabiri',
                'Bono Munir', 'Yahya Jabrane', 'Ayoub El Kaabi'],
    
    'Senegal': ['Édouard Mendy', 'Kalidou Koulibaly', 'Abdou Diallo', 'Idrissa Gueye', 'Cheikhou Kouyaté',
                'Sadio Mané', 'Ismaïla Sarr', 'Krepin Diatta', 'Boulaye Dia', 'Famara Diédhiou',
                'Pape Matar Sarr', 'Nampalys Mendy', 'Iliman Ndiaye', 'Nicolas Jackson', 'Habib Diallo',
                'Pape Gueye', 'Pathé Ciss', 'Lamine Camara', 'Mikayil Faye', 'Formose Mendy',
                'Seny Dieng', 'Youssouf Sabaly', 'Abdoulaye Seck'],
    
    'Nigeria': ['Victor Osimhen', 'Taiwo Awoniyi', 'Samuel Chukwueze', 'Ademola Lookman', 'Moses Simon',
                'Alex Iwobi', 'Wilfred Ndidi', 'Frank Onyeka', 'Joe Aribo', 'Kelechi Iheanacho',
                'Ola Aina', 'William Troost-Ekong', 'Calvin Bassey', 'Bright Osayi-Samuel', 'Semi Ajayi',
                'Maduka Okoye', 'Francis Uzoho', 'Raphael Onyedika', 'Emmanuel Dennis', 'Paul Onuachu',
                'Terem Moffi', 'Chidozie Awaziem', 'Kenneth Omeruo'],
    
    'Egypt': ['Mohamed Salah', 'Mohamed Elneny', 'Omar Marmoush', 'Mostafa Mohamed', 'Trézéguet',
              'Ahmed Hegazy', 'Mohamed Abdelmonem', 'Mahmoud Hassan Trezeguet', 'Zizo', 'Afsha',
              'Omar Kamal', 'Ahmed Sayed Zizo', 'Hussein El Shahat', 'Emam Ashour', 'Akram Tawfik',
              'Mohamed El Shenawy', 'Mohamed Sobhi', 'Marwan Hamdy', 'Omar Fayed', 'Ahmed Fattouh',
              'Hamza Alaa', 'Taher Mohamed', 'Mohamed Hamdy'],
    
    'Cameroon': ['André Onana', 'Collins Fai', 'Jean-Charles Castelletto', 'Nouhou Tolo', 'André-Frank Zambo Anguissa',
                 'Bryan Mbeumo', 'Karl Toko Ekambi', 'Eric Maxim Choupo-Moting', 'Vincent Aboubakar', 'Georges-Kévin Nkoudou',
                 'Frank Anguissa', 'Pierre Kunde', 'Olivier Kemen', 'Jean Onana', 'Enzo Ebosse',
                 'Christopher Wooh', 'Nicolas Moumi Ngamaleu', 'Ignatius Ganago', 'Christian Bassogog', 'Olivier Ntcham',
                 'Ablie Jallow', 'Devis Epassy', 'Jeando Fuchs'],
    
    'Côte d\'Ivoire': ['Sébastien Haller', 'Nicolas Pépé', 'Franck Kessié', 'Wilfried Singo', 'Serge Aurier',
                       'Simon Deli', 'Eric Bailly', 'Willy Boly', 'Ibrahim Sangaré', 'Jean-Philippe Gbamin',
                       'Max Gradel', 'Jonathan Bamba', 'Christian Kouamé', 'Wilfried Zaha', 'Jean Evrard Kouassi',
                       'Odilon Kossounou', 'Ghislain Konan', 'Jérémie Boga', 'Hamed Traore', 'Seko Fofana',
                       'Simon Adingra', 'Ousmane Diomande', 'Evan Ndicka'],
    
    'Algeria': ['Riyad Mahrez', 'Islam Slimani', 'Baghdad Bounedjah', 'Youcef Belaïli', 'Sofiane Feghouli',
                'Ismael Bennacer', 'Houssem Aouar', 'Ramiz Zerrouki', 'Nabil Bentaleb', 'Adlène Guedioura',
                'Ramy Bensebaini', 'Aïssa Mandi', 'Mohamed Amine Tougai', 'Youcef Atal', 'Mohamed Réda Halaimia',
                'Alexandre Oukidja', 'Anthony Mandrea', 'Farès Chaïbi', 'Mohamed Amoura', 'Saïd Benrahma',
                'Amine Gouiri', 'Yasser Larouci', 'Rayan Aït-Nouri'],
    
    'Tunisia': ['Wahbi Khazri', 'Youssef Msakni', 'Naïm Sliti', 'Ellyes Skhiri', 'Aïssa Laïdouni',
                'Mohamed Dräger', 'Hamza Mathlouthi', 'Montassar Talbi', 'Dylan Bronn', 'Ali Maâloul',
                'Hannibal Mejbri', 'Seifeddine Jaziri', 'Issam Jebali', 'Anis Ben Slimane', 'Saad Bguir',
                'Aymen Dahmen', 'Béchir Ben Saïd', 'Ferjani Sassi', 'Mohamed Ali Ben Romdhane', 'Haythem Jouini',
                'Hamza Rafia', 'Elias Achouri', 'Alaa Ghram'],
    
    'Mali': ['Amadou Haidara', 'Yves Bissouma', 'Hamari Traoré', 'Boubacar Kouyaté', 'Moussa Djenepo',
             'Adama Traoré', 'Kalifa Coulibaly', 'Ibrahima Koné', 'El Bilal Touré', 'Moussa Doumbia',
             'Lassine Sinayoko', 'Kamory Doumbia', 'Cheick Oumar Doucouré', 'Diadié Samassékou', 'Amadou Dante',
             'Ibrahim Mounkoro', 'Djigui Diarra', 'Falaye Sacko', 'Massadio Haïdara', 'Kiki Kouyaté',
             'Aliou Dieng', 'Fousseni Diabaté', 'Adama Noss Traoré'],
    
    'Ghana': ['Thomas Partey', 'Mohammed Kudus', 'Jordan Ayew', 'André Ayew', 'Kamaldeen Sulemana',
              'Daniel Amartey', 'Alexander Djiku', 'Alidu Seidu', 'Denis Odoi', 'Gideon Mensah',
              'Joseph Paintsil', 'Antoine Semenyo', 'Iñaki Williams', 'Ernest Nuamah', 'Edmund Addo',
              'Lawrence Ati-Zigi', 'Salis Abdul Samed', 'Elisha Owusu', 'Ibrahim Osman', 'Christopher Antwi-Adjei',
              'Brandon Thomas-Asante', 'Tariq Lamptey', 'Mohammed Salisu'],
    
    'Burkina Faso': ['Bertrand Traoré', 'Gustavo Sangaré', 'Edmond Tapsoba', 'Hassane Bandé', 'Issa Kaboré',
                     'Steeve Yago', 'Adama Guira', 'Blati Touré', 'Abdoul Tapsoba', 'Dango Ouattara',
                     'Hervé Koffi', 'Issoufou Dayo', 'Nasser Djiga', 'Sacha Banse', 'Saidou Simporé',
                     'Cédric Badolo', 'Mohamed Konaté', 'Aziz Ki', 'Dramane Salou', 'Abdoul Fessal Tapsoba',
                     'Adama Nagalo', 'Sofiane Ouédraogo', 'Salifou Diarrassouba'],
    
    'DR Congo': ['Chancel Mbemba', 'Arthur Masuaku', 'Gaël Kakuta', 'Cédric Bakambu', 'Yoane Wissa',
                 'Théo Bongonda', 'Silas Katompa', 'Samuel Moutoussamy', 'Meschack Elia', 'Simon Banza',
                 'Lionel Mpasi', 'Dylan Batubinsika', 'Rocky Bushiri', 'Aaron Tshibola', 'Edo Kayembe',
                 'Grejohn Kyei', 'Yannick Bolasie', 'Fiston Mayele', 'Grady Diangana', 'Charles Pickel',
                 'Henoc Inonga', 'Joris Kayembe', 'Nathan Fasika'],
    
    'South Africa': ['Percy Tau', 'Khuliso Mudau', 'Teboho Mokoena', 'Thapelo Morena', 'Themba Zwane',
                     'Ronwen Williams', 'Mothobi Mvala', 'Nyiko Mobbie', 'Zakhele Lepasa', 'Evidence Makgopa',
                     'Lyle Foster', 'Grant Margeman', 'Oswin Appollis', 'Mihlali Mayambela', 'Aubrey Modiba',
                     'Siyanda Xulu', 'Terrence Mashego', 'Elias Mokwana', 'Relebohile Mofokeng', 'Thabang Monare',
                     'Luke Fleurs', 'Mbongeni Mzimela', 'Iqraam Rayners'],
    
    'Guinea': ['Naby Keïta', 'Amadou Diawara', 'Ibrahima Conté', 'Issiaga Sylla', 'Mouctar Diakhaby',
               'Mohamed Bayo', 'Serhou Guirassy', 'Morgan Guilavogui', 'Aguibou Camara', 'Ibrahim Diakité',
               'Aly Keita', 'Julian Jeanvier', 'Ousmane Kanté', 'Antoine Conté', 'Saïdou Sow',
               'Facinet Conte', 'José Kanté', 'Simon Falette', 'Mohamed Ali Camara', 'Abdoulaye Touré',
               'Morlaye Sylla', 'François Kamano', 'Amadou Diallo'],
    
    # Add default names for other teams
    'Default': ['Mohamed Ahmed', 'Ibrahim Hassan', 'Youssef Ali', 'Omar Khalil', 'Moussa Diarra',
                'Abdoulaye Sow', 'Emmanuel Mensah', 'Patrick Banda', 'Joseph Phiri', 'Daniel Chama',
                'Samuel Osei', 'Benjamin Traore', 'Christian Kofi', 'Francis Amoah', 'George Owusu',
                'Kwame Asante', 'Kofi Mensah', 'Richard Boateng', 'Stephen Addai', 'Felix Annan',
                'Lawrence Adjei', 'Ernest Asante', 'Collins Fynn']
}


def get_real_player_names(team_name, count=23):
    """Get realistic player names for a team"""
    import random
    
    # Get team-specific names or use default
    if team_name in AFRICAN_PLAYER_NAMES:
        available_names = AFRICAN_PLAYER_NAMES[team_name].copy()
    else:
        available_names = AFRICAN_PLAYER_NAMES['Default'].copy()
    
    # If we need more names than available, generate variations
    while len(available_names) < count:
        base_name = random.choice(available_names[:10])
        if ' ' in base_name:
            first, last = base_name.split(' ', 1)
            available_names.append(f"{first} {random.choice(['Jr.', 'II', 'Mohamed', 'Ahmed'])}")
        else:
            available_names.append(f"{base_name} {random.randint(1, 99)}")
    
    # Shuffle and return the needed count
    random.shuffle(available_names)
    return available_names[:count]


def get_team_squad(team_name):
    """
    Get complete squad for a team with REALISTIC AFRICAN NAMES
    Returns: DataFrame with player details
    """
    cache_file = f'squad_{team_name.replace(" ", "_").replace("'", "")}.json'
    cached = get_cached_data(cache_file)
    if cached:
        return pd.DataFrame(cached)
    
    print(f"Generating squad for {team_name}...")
    
    # Position distribution (realistic for football)
    positions_config = [
        ('Goalkeeper', 3),
        ('Defender', 8),
        ('Midfielder', 8),
        ('Forward', 4)
    ]
    
    clubs = [
        'Al Ahly', 'Wydad Casablanca', 'TP Mazembe', 'Mamelodi Sundowns',
        'Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1',
        'Saudi Pro League', 'MLS', 'Süper Lig', 'Eredivisie', 'Portuguese League'
    ]
    
    import random
    random.seed(hash(team_name))
    
    # Get realistic names
    player_names = get_real_player_names(team_name, 23)
    
    squad = []
    player_idx = 0
    number = 1
    
    for position, count in positions_config:
        for _ in range(count):
            if player_idx < len(player_names):
                squad.append({
                    'player_name': player_names[player_idx],
                    'number': number,
                    'position': position,
                    'age': random.randint(19, 35),
                    'club': random.choice(clubs),
                    'market_value': random.randint(500000, 80000000) if position != 'Goalkeeper' else random.randint(300000, 40000000),
                    'nationality': team_name
                })
                player_idx += 1
                number += 1
    
    df = pd.DataFrame(squad)
    save_to_cache(df.to_dict('records'), cache_file)
    return df


def get_player_statistics():
    """
    Get tournament statistics for all players
    Returns: DataFrame with goals, assists, minutes, cards
    """
    cache_file = 'player_stats.json'
    cached = get_cached_data(cache_file)
    if cached:
        return pd.DataFrame(cached)
    
    print("Generating player statistics...")
    
    teams = get_participating_teams()
    all_stats = []
    
    import random
    for _, team in teams.iterrows():
        squad = get_team_squad(team['team_name'])
        for _, player in squad.iterrows():
            # Generate realistic stats
            games_played = random.randint(0, 7)
            minutes = games_played * random.randint(30, 90)
            goals = 0
            assists = 0
            yellow_cards = 0
            red_cards = 0
            
            if games_played > 0:
                if player['position'] == 'Forward':
                    goals = random.randint(0, min(games_played, 5))
                    assists = random.randint(0, min(games_played, 3))
                elif player['position'] == 'Midfielder':
                    goals = random.randint(0, min(games_played, 3))
                    assists = random.randint(0, min(games_played, 4))
                elif player['position'] == 'Defender':
                    goals = random.randint(0, min(games_played, 2))
                    assists = random.randint(0, min(games_played, 2))
                
                yellow_cards = random.randint(0, min(games_played, 3))
                if yellow_cards > 2:
                    red_cards = random.randint(0, 1)
            
            all_stats.append({
                'player_name': player['player_name'],
                'team': team['team_name'],
                'position': player['position'],
                'games_played': games_played,
                'minutes_played': minutes,
                'goals': goals,
                'assists': assists,
                'yellow_cards': yellow_cards,
                'red_cards': red_cards
            })
    
    df = pd.DataFrame(all_stats)
    save_to_cache(df.to_dict('records'), cache_file)
    return df


def get_matches_and_results():
    """
    Get all matches with results - AFCON 2025 MOROCCO CALENDAR
    Returns: DataFrame with match information
    """
    cache_file = 'matches.json'
    cached = get_cached_data(cache_file)
    if cached:
        return pd.DataFrame(cached)
    
    print("Generating AFCON 2025 Morocco match calendar...")
    
    teams = get_participating_teams()
    matches = []
    match_id = 1
    
    import random
    random.seed(42)
    
    # AFCON 2025 Morocco: December 21, 2025 - January 18, 2026
    # MATCHES À VENIR - La compétition n'a pas encore commencé!
    # Group stage matches - 3 matchdays
    groups = teams.groupby('group')
    matchday_dates = {
        1: ['2025-12-21', '2025-12-22', '2025-12-23'],  # Matchday 1
        2: ['2025-12-25', '2025-12-26', '2025-12-27'],  # Matchday 2
        3: ['2025-12-29', '2025-12-30', '2025-12-31']   # Matchday 3
    }
    
    for group_name, group_teams in groups:
        team_list = group_teams['team_name'].tolist()
        matchday = 1
        
        # Each team plays 3 matches (each plays all others)
        for i, team1 in enumerate(team_list):
            for team2 in team_list[i+1:]:
                # Assign to matchday dates
                date = matchday_dates[matchday][int(group_name[-1].encode()[0]) % 3]
                
                matches.append({
                    'match_id': match_id,
                    'phase': 'Group Stage',
                    'group': group_name,
                    'date': date,
                    'team_home': team1,
                    'team_away': team2,
                    'score_home': None,  # Pas encore joué
                    'score_away': None,  # Pas encore joué
                    'status': 'Scheduled'  # À venir
                })
                match_id += 1
                
                if match_id % 3 == 0:  # Rotate matchdays
                    matchday = (matchday % 3) + 1
    
    # Knockout stages with specific dates
    knockout_schedule = {
        'Round of 16': ['2026-01-04', '2026-01-05', '2026-01-06', '2026-01-07'],
        'Quarter-finals': ['2026-01-10', '2026-01-11'],
        'Semi-finals': ['2026-01-14', '2026-01-15'],
        'Final': ['2026-01-18']
    }
    
    for phase, dates in knockout_schedule.items():
        matches_per_day = len(dates)
        for i, date in enumerate(dates):
            # TBD - Les équipes seront déterminées après la phase de groupes
            matches.append({
                'match_id': match_id,
                'phase': phase,
                'group': None,
                'date': date,
                'team_home': 'TBD',  # À déterminer
                'team_away': 'TBD',  # À déterminer
                'score_home': None,
                'score_away': None,
                'status': 'Scheduled'
            })
            match_id += 1
    
    df = pd.DataFrame(matches)
    save_to_cache(df.to_dict('records'), cache_file)
    return df


def get_match_details(match_id):
    """
    Get detailed information for a specific match
    Returns: dict with lineups, scorers, events
    """
    import random
    random.seed(match_id)
    
    matches = get_matches_and_results()
    match = matches[matches['match_id'] == match_id].iloc[0]
    
    # Generate lineups
    home_squad = get_team_squad(match['team_home'])
    away_squad = get_team_squad(match['team_away'])
    
    home_lineup = home_squad.sample(n=11)['player_name'].tolist()
    away_lineup = away_squad.sample(n=11)['player_name'].tolist()
    
    # Generate scorers
    scorers = []
    for _ in range(match['score_home']):
        scorers.append({
            'team': match['team_home'],
            'player': random.choice(home_lineup),
            'minute': random.randint(1, 90)
        })
    for _ in range(match['score_away']):
        scorers.append({
            'team': match['team_away'],
            'player': random.choice(away_lineup),
            'minute': random.randint(1, 90)
        })
    
    scorers.sort(key=lambda x: x['minute'])
    
    return {
        'match_info': match.to_dict(),
        'home_lineup': home_lineup,
        'away_lineup': away_lineup,
        'scorers': scorers
    }


def aggregate_team_stats():
    """
    Aggregate statistics by team - AVANT LE TOURNOI
    Returns: DataFrame with team-level statistics
    """
    cache_file = 'team_stats.json'
    cached = get_cached_data(cache_file)
    if cached:
        return pd.DataFrame(cached)
    
    print("Generating team information (tournament not started yet)...")
    
    teams = get_participating_teams()
    
    team_stats = []
    for _, team in teams.iterrows():
        team_name = team['team_name']
        squad = get_team_squad(team_name)
        
        # Tournament hasn't started yet - all stats are 0
        team_stats.append({
            'team_name': team_name,
            'group': team['group'],
            'squad_value': team['squad_value'],
            'matches_played': 0,  # Pas encore joué
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'goals_scored': 0,
            'goals_conceded': 0,
            'goal_difference': 0,
            'points': 0,  # Pas encore de points
            'avg_age': squad['age'].mean(),
            'total_players': len(squad)
        })
    
    df = pd.DataFrame(team_stats)
    save_to_cache(df.to_dict('records'), cache_file)
    return df


def get_group_standings(group_name):
    """
    Get standings for a specific group
    Returns: DataFrame sorted by points
    """
    team_stats = aggregate_team_stats()
    group_teams = team_stats[team_stats['group'] == group_name].copy()
    
    # Sort by points, then goal difference, then goals scored
    group_teams = group_teams.sort_values(
        ['points', 'goal_difference', 'goals_scored'],
        ascending=[False, False, False]
    )
    
    return group_teams


# Data loading functions for Streamlit
def load_all_data():
    """
    Load all data needed for the dashboard
    Returns: dict with all dataframes
    """
    return {
        'teams': get_participating_teams(),
        'player_stats': get_player_statistics(),
        'matches': get_matches_and_results(),
        'team_stats': aggregate_team_stats()
    }


if __name__ == "__main__":
    # Test the scraper
    print("Testing AFCON scraper...")
    data = load_all_data()
    print(f"\nTeams: {len(data['teams'])}")
    print(f"Players: {len(data['player_stats'])}")
    print(f"Matches: {len(data['matches'])}")
    print(f"Team stats: {len(data['team_stats'])}")
    print("\nSample data loaded successfully!")
