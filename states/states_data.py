import csv
import numpy as np
import json

import pprint

################################################################################
# Global variables
qualified_players = {
    8: {},
    7: {},
    6: {}
}

players = {
    "Middle": [],
    "Elementary": []
}

PREZ_TOURNAMENT_DAYS = ["27-Sep_1", "4-Oct_2", "11-Oct_1", "18-Oct_2", "25-Oct_1", "1-Nov_2", "8-Nov_1", "15-Nov_2", "6-Dec_1", "13-Dec_2", "20-Dec_1", "10-Jan_2"]
SATURDAY_TOURNAMENT_MONTHS = ['Sept', 'Oct', 'Nov', 'Dec', 'Jan']
CUBE_GAMES = ['EQ', 'OS', 'Ling']

HIGHEST_PREZ_ELEMENTARY = 0
HIGHEST_PREZ_MIDDLE = 0
NUM_MIDDLE = 0
NUM_ELEMENTARY = 0
HIGHEST_MEAN_TABLE_MIDDLE = 0
HIGHEST_MEAN_TABLE_ELEMENTARY = 0

################################################################################
# Saturday 
def get_saturday_tournament_info(grade, playerName, month, data_type, data):
    qualified_players[grade][playerName]['Saturday_Tournaments'][month][data_type] = data

def insert_saturday_tournament_data(row, grade):
    playerName = row['FirstName'] + " " + row['LastName']
    qualified_players[grade][playerName] = {}
    qualified_players[grade][playerName]['Name'] = playerName
    qualified_players[grade][playerName]['Saturday_Tournaments'] = {}
    for month in SATURDAY_TOURNAMENT_MONTHS:
        if row[month]:
            qualified_players[grade][playerName]['Saturday_Tournaments'][month] = {}
            get_saturday_tournament_info(grade, playerName, month, 'score', int(row[month]))
            get_saturday_tournament_info(grade, playerName, month, 'table', int(row[month + 'Table']))
            get_saturday_tournament_info(grade, playerName, month, 'game', row[month + 'Game'])

def get_saturday_tournament_data(input_file):
    with open(input_file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            insert_saturday_tournament_data(row, int(row['Grade']))


################################################################################
# Prez 
def insert_prez_data(grade, playerName, date, score):
    qualified_players[grade][playerName]["Prez"][date] = score

def insert_prez_progression(row, grade):
    playerName = row['FirstName'] + " " + row['LastName']
    if playerName in qualified_players[grade]:
        qualified_players[grade][playerName]["Prez"] = {}
        for date in PREZ_TOURNAMENT_DAYS:
            if row[date]:
                insert_prez_data(grade, playerName, date, int(row[date]))

def get_prez_progression(input_file):
    with open(input_file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            insert_prez_progression(row, int(row['Grade']))


################################################################################
# Friday
def get_friday_info(grade, playerName, dictionary_name, label, data):
    qualified_players[grade][playerName][dictionary_name][label].append(int(data))

def insert_friday_data(row, grade):
    playerName = row['FirstName'] + " " + row['LastName']
    if playerName in qualified_players[grade]:
        # Friday tournaments
        qualified_players[grade][playerName]['Friday_Tournaments'] = {}
        for game in CUBE_GAMES:
            if game[:2] in [key[:2] for key, val in row.items() if (key[-2:] != 'CM') and (key[-2:] != 'ts') and (key[-2:] != 'me') and (key[-2:] != 'de')]:
                qualified_players[grade][playerName]['Friday_Tournaments'][game] = []
                for i in range(1, 6):
                    if len(row[game + str(i)]) > 0:
                        get_friday_info(grade, playerName, 'Friday_Tournaments', game, row[game + str(i)])
        # Challenge Matches
        qualified_players[grade][playerName]['Challenge_Matches'] = {}
        for game in CUBE_GAMES:
            if game + '_CM' in row and len(row[game + '_CM']) > 0:
                qualified_players[grade][playerName]['Challenge_Matches'][game] = []
                get_friday_info(grade, playerName, 'Challenge_Matches', game, row[game + '_CM'])
        # Worksheets
        qualified_players[grade][playerName]['Worksheets'] = {}
        for game in CUBE_GAMES:
            if game + '_Worksheets' in row and len(row[game + '_Worksheets']) > 0:
                qualified_players[grade][playerName]['Worksheets'][game] = []
                get_friday_info(grade, playerName, 'Worksheets', game, row[game + '_Worksheets'])

def get_cube_game_scores(input_file):
    with open(input_file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            insert_friday_data(row, int(row['Grade']))

#
###############################################################################
# Rankings
def get_rank_data(grade, playerName, rank_type, rank):
    qualified_players[grade][playerName]["Rankings"][rank_type] = rank

def insert_rank_data(row, grade):
    playerName = row['FirstName'] + " " + row['LastName']
    if playerName in qualified_players[grade]:
        qualified_players[grade][playerName]["Rankings"] = {}
        get_rank_data(grade, playerName, 'saturday_rank', float(row['Saturdays']))
        get_rank_data(grade, playerName, 'friday_rank', float(row['Fridays']))
        get_rank_data(grade, playerName, 'total_rank', float(row['Total']))

def get_rankings(input_file):
    global NUM_ELEMENTARY
    global NUM_MIDDLE
    with open(input_file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row['Grade'] == '6':
                NUM_ELEMENTARY += 1
            else:
                NUM_MIDDLE += 1
            insert_rank_data(row, int(row['Grade']))

################################################################################
# Saving stuff
def clean_saturday_data(person_data, grade):
    global HIGHEST_MEAN_TABLE_ELEMENTARY
    global HIGHEST_MEAN_TABLE_MIDDLE
    if 'Saturday_Tournaments' in person_data:
        saturday_scores = []
        saturday_tables = []
        for month in SATURDAY_TOURNAMENT_MONTHS:
            if month in person_data['Saturday_Tournaments']:
                for saturday_tournament_data_name, saturday_tournament_data in person_data['Saturday_Tournaments'][month].items():
                    if saturday_tournament_data_name == 'score':
                        saturday_scores.append(saturday_tournament_data)
                    if saturday_tournament_data_name == 'table':
                        saturday_tables.append(saturday_tournament_data)
        person_data['Saturday_Tournaments']['saturday_scores'] = saturday_scores
        person_data['Saturday_Tournaments']['saturday_mean_score'] = float(np.mean(saturday_scores))
        person_data['Saturday_Tournaments']['saturday_tables'] = saturday_tables
        person_data['Saturday_Tournaments']['saturday_mean_table'] = float(np.mean(saturday_tables))
        person_data['Saturday_Tournaments']['num_sat_tournaments'] = len(saturday_scores)
        person_data['Saturday_Tournaments']['saturday_top_3'] = int(np.sum(sorted(saturday_scores, reverse=True)[:3]))
        person_data['Saturday_Tournaments']['saturday_top_3_mean'] = float(np.mean(sorted(saturday_scores, reverse=True)[:3]))
        mean_table = person_data['Saturday_Tournaments']['saturday_mean_table']
        if grade == 6:
            if HIGHEST_MEAN_TABLE_ELEMENTARY < mean_table:
                HIGHEST_MEAN_TABLE_ELEMENTARY = mean_table
        else:
            if HIGHEST_MEAN_TABLE_MIDDLE < mean_table:
                HIGHEST_MEAN_TABLE_MIDDLE = mean_table

def clean_prez_data(person_data, grade):
    global HIGHEST_PREZ_ELEMENTARY
    global HIGHEST_PREZ_MIDDLE
    if 'Prez' in person_data:
        prez_scores = []
        first_half = []
        second_half = []
        for prez_date, prez_score in person_data['Prez'].items():
            prez_scores.append(prez_score)
            if prez_date[-1] == "1":
                first_half.append(prez_score)
            else:
                second_half.append(prez_score)
        person_data['Prez']['prez_scores'] = prez_scores
        person_data['Prez']['prez_mean'] = float(np.mean(prez_scores))
        person_data['Prez']['prez_total'] = int(np.sum(prez_scores))
        person_data['Prez']['prez_first_half'] = first_half
        person_data['Prez']['prez_second_half'] = second_half
        if grade == 6:
            if person_data['Prez']['prez_mean'] > HIGHEST_PREZ_ELEMENTARY:
                HIGHEST_PREZ_ELEMENTARY = person_data['Prez']['prez_mean']
        else:
            if person_data['Prez']['prez_mean'] > HIGHEST_PREZ_MIDDLE:
                HIGHEST_PREZ_MIDDLE = person_data['Prez']['prez_mean']

def clean_friday_data(person_data):
    if 'Friday_Tournaments' in person_data:
        for game in CUBE_GAMES:
            if game in person_data['Friday_Tournaments']:
                data = person_data['Friday_Tournaments'][game]
                person_data['Friday_Tournaments'][game + '_num_matches'] = len(data)
                person_data['Friday_Tournaments'][game + '_total'] = int(np.sum(data))
                if len(data) > 0:
                    person_data['Friday_Tournaments'][game + '_mean'] = float(np.mean(data))
                else:
                    person_data['Friday_Tournaments'][game + '_mean'] = 0

def clean_worksheet_data(person_data):
    if 'Worksheets' in person_data:
        total_worksheet_score = 0
        for game in CUBE_GAMES:
            if game in person_data['Worksheets']:
                person_data['Worksheets'][game] = person_data['Worksheets'][game][0]
                total_worksheet_score += person_data['Worksheets'][game]
        person_data['Worksheets']['total'] = total_worksheet_score

def calculate_sweeps(person_data, grade):
    # EQ + OS + Ling + Prez
    person_data['sweeps'] = 0
    person_data['sweeps_calculation'] = {}
    if 'Friday_Tournaments' in person_data:
        for game in CUBE_GAMES:
            # scale to 24
            if game in person_data['Friday_Tournaments']:
                scaled_score = (person_data['Friday_Tournaments'][game + '_mean'] / 6) * 24
                person_data['sweeps'] += scaled_score
                person_data['Friday_Tournaments'][game + '_scaled'] = scaled_score
                person_data['sweeps_calculation'][game] = scaled_score
        person_data['sweeps_no_prez'] = person_data['sweeps']
    if 'Prez' in person_data:
        # scale to 25 relative to highest score
        if grade == 6:
            scaled_score = (float(person_data['Prez']['prez_mean']) / HIGHEST_PREZ_ELEMENTARY) * 25
        else:
            scaled_score = (float(person_data['Prez']['prez_mean']) / HIGHEST_PREZ_MIDDLE) * 25
        person_data['Prez']['prez_scaled'] = scaled_score
        person_data['sweeps_calculation']['prez'] = scaled_score
        person_data['sweeps'] += scaled_score 
    if 'Rankings' in person_data:
        if grade == 6:
            person_data['adjusted_sweeps'] = \
                person_data['sweeps'] + \
                (((NUM_ELEMENTARY * 2) - person_data['Rankings']['total_rank']) * 2) + \
                (HIGHEST_MEAN_TABLE_ELEMENTARY - person_data['Saturday_Tournaments']['saturday_mean_table']) + \
                (person_data['Saturday_Tournaments']['saturday_top_3_mean'])
        else:
            person_data['adjusted_sweeps'] = \
                person_data['sweeps'] + \
                (((NUM_MIDDLE * 2) - person_data['Rankings']['total_rank']) * 2) + \
                (HIGHEST_MEAN_TABLE_MIDDLE - person_data['Saturday_Tournaments']['saturday_mean_table']) + \
                (person_data['Saturday_Tournaments']['saturday_top_3_mean'])


def clean_data():
    for grade, data in qualified_players.items():
        for person, person_data in data.items():
            clean_saturday_data(person_data, grade)
            clean_prez_data(person_data, grade)
            clean_friday_data(person_data)
            clean_worksheet_data(person_data)
    for grade, data in qualified_players.items():
        for person, person_data in data.items():
            calculate_sweeps(person_data, grade)


def split_into_divisions():
    for grade, data in qualified_players.items():
        for person, person_data in data.items():
            if grade == 6:
                players['Elementary'].append(person_data)
            else:
                players['Middle'].append(person_data)

################################################################################
# Main
get_saturday_tournament_data('2019-2020/saturday_tournaments.csv')
get_prez_progression('2019-2020/prez_progression.csv')
get_cube_game_scores('2019-2020/individual_rankings.csv')
get_rankings('2019-2020/rankings.csv')

clean_data()
split_into_divisions()

# pprint.pprint(qualified_players)
with open('data.json', 'w') as f:
    json.dump(players, f)
