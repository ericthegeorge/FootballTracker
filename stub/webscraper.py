import requests
from bs4 import BeautifulSoup
import time
import csv


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
                print(club_name)
    
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
        time.sleep(1)  # polite crawling

    return all_players, club_links


def save_to_csv(data, filename="players.csv"):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
        
league_url = 'https://en.soccerwiki.org/league.php?leagueid=89'
players, clubs = scrape_league(league_url=league_url)

playersd = []
clubsd = []
clubsd = []

for club_name, club_url, manager_name, location, logo_src in clubs:
    clubsd.append({
        "name": club_name,
        "url": club_url,
        "manager": manager_name,
        "location": location,
        "logo": logo_src
    })

for club_name, player_name, player_url in players:
    playersd.append({"club": club_name, "player": player_name, "url": player_url})


save_to_csv(playersd)
save_to_csv(clubsd)