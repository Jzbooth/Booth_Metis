"""
Scrape ESPN's weekly fantasy football projections and actual scoring.
"""
from itertools import chain
from bs4 import BeautifulSoup
from csv import DictWriter
from time import sleep
import requests
import sys

USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'}
PROJ_URL = ('http://games.espn.go.com/ffl/tools/projections'
            '?&scoringPeriodId={}&seasonId={}&startIndex={}')
SCORING_URL = ('http://games.espn.go.com/ffl/leaders'
                '?&scoringPeriodId={}&seasonId={}&startIndex={}')
GAMELOG_URL = 'http://espn.go.com/nfl/player/gamelog/_/id/{}'
# stats on the gamelog page are position specific
# create a mapping of player position to column headers
HEADER_MAPPING = {
    'QB': ['date', 'opponent', 'result', 'pass_completions', 'pass_attempts',
            'pass_yards', 'completion_percentage', 'pass_yards_per_attempt',
            'longest_pass', 'pass_TD', 'interceptions', 'qb_rating',
            'passer_rating'],
    'RB': ['date', 'opponent', 'result', 'rush_attempts', 'rush_yards',
            'rush_yards_per_attempt', 'longest_run', 'rush_TD', 'receptions',
            'receiving_yards', 'yards_per_reception', 'longest_reception',
            'receiving_TDs', 'fumbles', 'fumbles_lost'],
    'WR': ['date', 'opponent', 'result', 'receptions', 'targets',
            'receiving_yards', 'yards_per_reception', 'longest_reception',
            'receiving_TDs', 'rush_attempts', 'rush_yards',
            'rush_yards_per_attempt', 'longest_run', 'rush_TD',
            'fumbles', 'fumbles_lost'],
    'TE': ['date', 'opponent', 'result', 'receptions', 'targets',
            'receiving_yards', 'yards_per_reception', 'longest_reception',
            'receiving_TDs', 'rush_attempts', 'rush_yards',
            'rush_yards_per_attempt', 'longest_run', 'rush_TD',
            'fumbles', 'fumbles_lost'],
    'PK': ['date', 'opponent', 'result', '1-19', '20-29', '30-39', '40-49',
            '50+', 'fg_totals', 'percentage', 'avg_distance',
            'longest_made', 'extra_points_made', 'extra_point_attempts',
            'points'],
    'DST': [] # no such thing as "gamelogs" for DST - have to parse all stats
}


def get_projections(week, season, num_players=400, wait=0, timeout=60):
    projections = []
    for i in range(0, num_players + 1, 40):
        response = requests.get(PROJ_URL.format(week, season, i),
                                headers=USER_AGENT,
                                timeout=timeout)
        
        try:
            response.raise_for_status()
        except HTTPError:
            # ESPN is throwing random 404s - let's at least try twice
            print('HTTPError; trying again: {}'.format(response.url))
            response = requests.get(PROJ_URL.format(week, i),
                                    headers=USER_AGENT,
                                    timeout=timeout)
            response.raise_for_status()

        msg = 'Fetching projections for week {}, {}, {} of {}: ({}) {}'
        print(msg.format(week, season, i, num_players, response.status_code, response.url))
        
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find('table', class_='playerTableTable')

        for row in table.find_all('tr', 'pncPlayerRow'):
            try:
                projections.append({
                    'season': float(season),
                    'week': float(week),
                    'player_id': float(row.find_all('td')[0].a.get('playerid')),
                    'name': row.find_all('td')[0].a.text.strip(),
                    'opponent': row.find_all('td')[1].text.strip(),
                    'game_result': row.find_all('td')[2].text.strip(),
                    'pass_completions': float(row.find_all('td')[3].text.split('/')[0]),
                    'pass_attempts': float(row.find_all('td')[3].text.split('/')[1]),
                    'pass_yards': float(row.find_all('td')[4].text),
                    'pass_TD': float(row.find_all('td')[5].text),
                    'interceptions': float(row.find_all('td')[6].text),
                    'rush_attempts': row.find_all('td')[7].text,
                    'rush_yards': float(row.find_all('td')[8].text),
                    'rush_TD': float(row.find_all('td')[9].text),
                    'receptions': float(row.find_all('td')[10].text),
                    'receiving_yards': float(row.find_all('td')[11].text),
                    'receiving_TD': float(row.find_all('td')[12].text),
                    'projected_pts': float(row.find_all('td')[13].text),
                })
            except IndexError: # handle players on BYE week
                continue
        sleep(wait) # ESPN was throwing 404s, but the page loads when testing
    return projections
