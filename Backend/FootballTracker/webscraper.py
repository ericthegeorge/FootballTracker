import requests
from bs4 import BeautifulSoup
import time as tttime
import csv
import random
from datetime import date, time, timedelta
from django_countries.fields import CountryField
from django_countries import countries

import django

import os
import django
import sys

# This should point to your 'Backend' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()


from footballtracker.models import *

BASE_URL = "https://en.soccerwiki.org"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_club_links_from_league(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    clubs = []
    seen_urls = set()

    for td in soup.select('td.text-left'):
        a_tag = td.find('a', href=True)
        if a_tag and "clubid" in a_tag['href']:
            club_name = a_tag.get_text(strip=True)
            club_href = a_tag['href']
            club_url = BASE_URL + club_href

            if club_url not in seen_urls:
                # Manager
                tdmanager = td.find_next_sibling()
                manager_name = None
                if tdmanager:
                    a_tagmanager = tdmanager.find('a', href=True)
                    if a_tagmanager:
                        manager_name = a_tagmanager.get_text(strip=True)

                # Location
                tdlocation = tdmanager.find_next_sibling() if tdmanager else None
                location = None
                if tdlocation:
                    a_taglocation = tdlocation.find('a', href=True)
                    if a_taglocation:
                        location = a_taglocation.get_text(strip=True)

                # Logo
                tdlogo = td.find_previous_sibling()
                logo_src = None
                if tdlogo:
                    img_tag = tdlogo.find('img')
                    if img_tag:
                        logo_src = img_tag.get('src')

                seen_urls.add(club_url)
                clubs.append((club_name, club_url, manager_name, location, logo_src))
                # clubs.append({"club": club_name, })
                # print(club_name)
    
    return clubs


def get_players_from_club(club_url, club_name):
    response = requests.get(club_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    player_data = []

    for td in soup.select("td.text-left.text-dark")[1:]:  # skip header row
        a_tag = td.find('a', href=True)
        if a_tag and "player" in a_tag['href']:
            player_name = a_tag.get_text(strip=True)
            player_href = a_tag['href']
            player_url = BASE_URL + player_href
            # player_data.append({"club": club_name, "player": player_name, "url": player_url})
            player_data.append((club_name, player_name, player_url))
    return player_data


def scrape_league(league_url):
    all_players = []
    club_links = get_club_links_from_league(league_url)
    
    for club_name, club_url, manager_name, location, logo_src in club_links:
        print(f"Scraping club: {club_url}")
        players = get_players_from_club(club_url, club_name)
        all_players.extend(players)
        tttime.sleep(1)  # polite crawling

    return all_players, club_links


def save_to_csv(data, filename="players.csv"):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
        
league_url = 'https://en.soccerwiki.org/league.php?leagueid=89'
playerss, clubs = scrape_league(league_url=league_url)

playersd = []

def getRandomPositions():
    return random.sample(["Goalkeeper", "Defender", "Midfielder", "Forward"], k=random.randint(1, 3))


def outgoalDict():
    outfield = random.randint(1,2)
    if (outfield == 1):
        return {
            "goals" : random.randint(1, 100),
            "assists": random.randint(1, 250),
            "penalties_scored": random.randint(1, 50)
        }
    else:
        return {
            "goals_conceded": random.randint(1, 100),
            "goals_saved": random.randint(1, 100),
            "clean_sheets": random.randint(1, 25),
            "penalties_saved": random.randint(1, 25)
        }

# Player_ID Name DOB Minutes_Played Matches_Played Market_Value Preferred_Foot Height Yellow_Cards Red_Cards Playing_Team_Name Owning_Team_Name
for club_name, player_name, player_url in playerss:
    playersd.append(
        {"name": player_name,
         "dob": random.randint(1970, 2005),
        "minutes_played": random.randint(1000, 3000), 
        "matches_played": random.randint(10, 40),  
        "market_value": round(random.uniform(5.0, 100.0), 2), 
        "preferred_foot": random.choice(["Left", "Right"]),  
        "height": round(random.uniform(1.65, 2.00), 2),  
        "yellow_cards": random.randint(0, 15),  
        "red_cards": random.randint(0, 5),
        "playing_team": club_name,
        "owning_team": club_name,
        "positions": getRandomPositions(), # Playing team is the club
        "nationality": random.sample([code for code, _ in countries], 2),
        "url": player_url})
    playersd[-1].update(outgoalDict())

# print(playersd)

clubsd = []

def random_date(start_year, end_year):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    delta = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, delta))


for club_name, club_url, manager_name, location, logo_src in clubs:
    clubsd.append({
        "name": club_name,
        "url": club_url,
        "manager_name": manager_name,
        "home_ground": location,
        "manager_dob": random_date(1970, 2005),
        "manager_date_joined": random_date(2005, 2024),
        "manager_seasons_headed": random.randint(1, 12),
        "image": logo_src,
        "manager_nationality": random.sample([code for code, _ in countries], 2)
    })







def get_country_code(name):
    for code, country_name in countries:
        if country_name.lower() == name.lower():
            return code
    return "ES"  # Or "XX" as a fallback



def create_stub_data():
    # Create leagues
    league = League.objects.create(name="FIFA")
    
    # Create teams
    teams = []
    for club in clubsd:
        team = Team.objects.create(
            name=club["name"],
            manager_name=club["manager_name"] or "John Doe",
            manager_dob=club["manager_dob"],
            manager_date_joined=club["manager_date_joined"],
            manager_seasons_headed=club["manager_seasons_headed"],
            home_ground=club["home_ground"] or "Bilbao",
            image=club["image"]
        )
        TeamPlaysInLeague.objects.create(team=team, league=league)
        teams.append(team)



    # Create players
    players = []
    for pdata in playersd:
        team = next((t for t in teams if t.name == pdata["playing_team"]), None)
        if team:
            player = Player.objects.create(
                name=pdata["name"],
                dob=date(pdata["dob"], 1, 1),
                minutes_played = pdata["minutes_played"],
                matches_played = pdata["matches_played"],
                market_value = pdata["market_value"],
                preferred_foot=pdata["preferred_foot"],
                height=pdata["height"],
                yellow_cards = pdata["yellow_cards"],  
                red_cards = pdata["red_cards"],
                playing_team = team,
                owning_team = team,
            )
            if ("goals" in pdata):
                OutfieldPlayer.objects.create(
                    player = player,
                    assists=pdata["assists"],
                    goals=pdata["goals"],
                    penalties_scored=pdata["penalties_scored"]
                )
            else:
                Goalkeeper.objects.create(
                    player = player,
                    goals_conceded=pdata["goals_conceded"],
                    goals_saved=pdata["goals_saved"],
                    clean_sheets=pdata["clean_sheets"],
                    penalties_saved = pdata["penalties_saved"],
                )
            for nationality in pdata["nationality"]:
                PlayerNationality.objects.create(
                    player = player,
                    nationality = nationality
                )

            PlayerPlaysForTeam.objects.create(player=player, team=team, shirt_number=random.randint(1, 99))
            players.append((player, team))


    match = Match.objects.create(
        date=date.today(),
        location="Wembley Stadium",
        start_time=time(15, 0),
        end_time=time(17, 0),
        referee_name="John Doe"
    )



    MatchHeldInLeague.objects.create(match=match, league=league)
    MatchRefereeNationality.objects.create(match=match, nationality="ES")

    # Create match data for teams
    for team in teams[:2]:  # only 2 teams per match
        TeamMatchData.objects.create(
            match=match,
            team=team,
            stoppage_time=random.randint(0, 5),
            had_extra_time=random.choice([True, False]),
            had_penalties=random.choice([True, False]),
            goals_conceded=random.randint(0, 3),
            saves=random.randint(0, 10),
            offsides=random.randint(0, 5),
            goals_scored=random.randint(0, 3),
            shots_on_target=random.randint(0, 10),
            possession_percentage=random.uniform(40.0, 60.0),
            completed_passes=random.randint(200, 500),
            total_passes=random.randint(300, 600),
            match_outcome=random.choice(["Win", "Loss", "Draw"]),
            team_formation=random.choice(["4-4-2", "4-3-3", "3-5-2"])
        )
        TeamMatch.objects.create(
            team = team,
            match = match,
        )

    # Create player data
    for player, team in players[:22]:  # limit to 22 players for match
        PlayerMatchData.objects.create(
            match=match,
            player=player,
            stoppage_time=random.randint(0, 5),
            had_extra_time=random.choice([True, False]),
            had_penalties=random.choice([True, False]),
            assists=random.randint(0, 3),
            completed_passes=random.randint(20, 80),
            total_passes=random.randint(30, 100),
            minutes_played=random.randint(60, 120),
            goals_scored=random.randint(0, 3),
            shots_on_target=random.randint(0, 5),
            total_shots=random.randint(0, 8),
            fouls=random.randint(0, 4),
            goals_conceded=random.randint(0, 2),
            saves=random.randint(0, 5),
            position=random.choice([p[0] for p in Position.choices])
        )
        PlayerMatch.objects.create(
            player = player,
            match = match,
        )


create_stub_data()
