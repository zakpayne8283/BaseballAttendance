import os
import pandas as pd
import time
from urllib.error import HTTPError

class DataHelper():

    # 'Team Name': ['Abbreviations']
    # Some teams have moved or changed names, so abbreviations differ
    teams = {
        'Diamondbacks': ['ARI'],
        'Athletics': ['OAK', 'ATH'],
        'Braves': ['ATL'],
        'Orioles': ['BAL'],
        'Red Sox': ['BOS'],
        'Cubs': ['CHC'],
        'White Sox': ['CHW'],
        'Reds': ['CIN'],
        'Guardians': ['CLE'],
        'Rockies': ['COL'],
        'Tigers': ['DET'],
        'Astros': ['HOU'],
        'Royals': ['KCR'],
        'Angels': ['ANA', 'LAA'],
        'Dodgers': ['LAD'],
        'Marlins': ['FLA', 'MIA'],
        'Brewers': ['MIL'],
        'Twins': ['MIN'],
        'Mets': ['NYM'],
        'Yankees': ['NYY'],
        'Phillies': ['PHI'],
        'Pirates': ['PIT'],
        'Padres': ['SDP'],
        'Giants': ['SFG'],
        'Mariners': ['SEA'],
        'Cardinals': ['STL'],
        'Rays': ['TBD', 'TBR'],
        'Rangers': ['TEX'],
        'Blue Jays': ['TOR'],
        'Nationals': ['MON', 'WSN']
    }
    
    start_year = 2000
    end_year   = 2025

    suppress_print_output = False

    output_file = 'raw_output.csv'

    base_schedule_url = 'https://www.baseball-reference.com/teams/[[TEAM]]/[[YEAR]]-schedule-scores.shtml'

    def __init__(self, **kwargs):
        kw_options = ['start_year', 'end_year', 'suppress_print_output']

        for opt in kw_options:
            if opt in kwargs.keys():
                setattr(self, opt, kwargs[opt])

            print(f'Using {opt}={self.__getattribute__(opt)}')


        print('Created DataHelper!')

    
    def collect_data(self):
        for team, codes in self.teams.items():
            print(f'Collecting Data for {team}...')

            for team_code in codes:
                for year in range(self.start_year, self.end_year+1):
                    print(f'Downloading {year}...', end='', flush=True)

                    target_url = self.base_schedule_url.replace('[[TEAM]]', team_code).replace('[[YEAR]]', str(year))

                    # Download the data
                    try:
                        pd.read_html(target_url)[0].to_csv(self.output_file, mode='a', header=not os.path.exists(self.output_file), index=False)
                        print(' Done!')
                    except HTTPError as e:
                        print(f'Failed to fetch {year} for {team_code}!')

                    # baseball-reference rate limits you.
                    # Too many requests (about 20/minute) locks you out for 30 minutes
                    time.sleep(5)

            print(f'Finished {team}')

        print(f'Finished Collecting All Data!')
