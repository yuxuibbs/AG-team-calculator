import pandas as pd
import numpy as np
import re
import helper_functions

def split_games(col1, col2, games):
    if len(games) == 3:
        return col1.where(col2.str.endswith(games[0], na=False) | col2.str.endswith(games[1], na=False) | col2.str.endswith(games[2], na=False))
    else:
        return col1.where(col2.str.endswith(games[0], na=False) | col2.str.endswith(games[1], na=False))

def change_data(fileName, sheet_name, columns, key, cols_to_remove):
    '''
    Reads an excel file and cleans it up

    Arguments:
        fileName {string} -- input file name
        sheet_name {number or string} -- sheet name to read from the excel file
        columns {list} -- list of column strings for the excel file
        key {string} -- column name that every student has that summary statistics on the bottom of the excel file doesn't have
        cols_to_remove {list} -- columns to remove from the final data
    
    Returns:
        pandas data frame -- cleaned up version of the data in the excel file
    '''
    data = helper_functions.read_input_file(fileName, sheet_name)
    data.columns = columns
    data = helper_functions.fix_names(helper_functions.remove_unnecessary_rows(data, key, cols_to_remove)).replace(r'^\s*$', np.nan, regex=True)
    return data

satTourn = change_data('Clague 18.xlsx', 
                        0, 
                        ['FirstName', 'LastName', 'Grade', 'Sept', 'SeptTableNum', 'SeptGame', 'Oct', 'OctTableNum', 'OctGame', 'Nov', 'NovTableNum', 'NovGame', 'Dec', 'DecTableNum', 'DecGame', 'Jan', 'JanTableNum', 'JanGame', 'Feb', 'FebTableNum', 'FebGame', 'Total', 'Avg', 'TableAvg', 'AvgWithTableBump', 'AdjAvg'], 
                        'FirstName', 
                        ['Total', 'Avg', 'TableAvg', 'AvgWithTableBump', 'AdjAvg', "Feb", "FebTableNum", "FebGame"])

friTourn = change_data('Clic1819.xlsx',
                        'Individual Standings',
                        ['FirstName', 'LastName', 'Grade', 'Team', 'EQ1', 'EQ2', 'EQ3', 'EQ4', 'EQ_CM', 'EQ5', 'OS1', 'OS2', 'OS3', 'OS4', 'OS_CM', 'OS5', 'EQ_Worksheets', 'Ling1', 'Ling2', 'Ling_CM', 'Ling3', 'OS_Worksheets', 'Ling4', 'Ling5', 'Ling_Worksheets', 'Mixed', 'Mixed', 'Mixed', 'Mixed', 'Mixed', 'Mixed', 'Total', 'EQTotal', 'OSTotal', 'LingTotal', 'PropTotal', 'PresTotal', 'TournamentTotal', 'Avg', 'Challenge Match', 'Worksheets', 'WorksheetsRemaining', 'Mixed', 'Mixed'],
                        'Grade', 
                        ['Total', 'EQTotal', 'OSTotal', 'LingTotal', 'PropTotal', 'PresTotal', 'TournamentTotal', 'Avg', 'Challenge Match', 'Worksheets', 'WorksheetsRemaining', 'Mixed']
                        )
prezProg = change_data('Pres Progression1819.xlsx',
                        'Sheet1',
                        ['FirstName', 'LastName', 'Grade', '28-Sep_1', '5-Oct_2', '12-Oct_1', '26-Oct_1', '2-Nov_2', '9-Nov_1', '16-Nov_2', '30-Nov_1', '14-Dec_2', '21-Dec_1', '11-Jan_2', '1-Feb_1', '8-Feb_2', '22-Feb_1', 'Total'],
                        'FirstName', 
                        ['Total', "1-Feb_1", "8-Feb_2", "22-Feb_1"])



# join data by full name
all_data = satTourn.set_index('FullName').join(friTourn.set_index('FullName'), lsuffix='Grade')

# remove duplicate and irrelevant info
all_data = all_data.drop(["GradeGrade", "Team"], axis=1)


# Feb is OEO, Jan is EOE, Dec is OEO, Nov is EOE, Oct is OEO
MONTHS = ['Sept', 'Oct', 'Nov', 'Dec', 'Jan']
# EQ, OS, Ling
GAMES = { 'EQ': ['AE', 'B2', 'LEO'], 
          'OS': ['OS', 'B2', 'LEO'], 
          'Ling': ['Ling', 'LEO'] }
for month in MONTHS:
    for game in GAMES:
        all_data[month + game] = split_games(all_data[month], all_data[month + 'Game'], GAMES[game])

# Friday info
for game in GAMES:
    all_data[game + 'FriTot'] = all_data.filter(regex=game + '\d').astype(float).sum(axis=1)
    all_data[game + 'FriNum'] = all_data.filter(regex=game + '\d').count(axis=1)


# Saturday info
satGameData = all_data.loc[:, 'SeptEQ':'JanLing']
for game in GAMES:
    all_data[game + 'SatAvg'] = satGameData.filter(regex=game).astype(float).mean(axis=1)
    all_data[game + 'SatSum'] = satGameData.filter(regex=game).astype(float).sum(axis=1)
    all_data[game + 'SatNum'] = satGameData.filter(regex=game).astype(float).count(axis=1)

all_data['SatTableNum'] = all_data.filter(regex='TableNum').astype(float).mean(axis=1)


# calculate average score for each game
for game in GAMES:
    all_data[game + 'OverallAvg'] = (all_data[game + 'FriTot'] + all_data[game + 'SatSum']) / (all_data[game + 'FriNum'] + (all_data[game + 'SatNum']) * 3)
    all_data[game + 'OverallAvg'].fillna(0, inplace=True)
# fill NaN values
for game in GAMES:
    match_string = game + r'\d'
    game_cols = [x for x in all_data.columns if re.match(match_string, x)]
    all_data[game_cols] = all_data.filter(regex=match_string).where(pd.notnull(all_data.filter(regex=match_string)), all_data[game + 'OverallAvg'], axis='rows')
    
    match_string = r'\D+' + game
    game_cols = [x for x in all_data.columns if re.match(match_string, x)]
    all_data[game_cols] = all_data.filter(regex=match_string).where(pd.notnull(all_data.filter(regex=match_string)), all_data[game + 'OverallAvg'] * 3, axis='rows')
    
    match_string = game + '_Worksheets'
    game_cols = [x for x in all_data.columns if re.match(match_string, x)]
    all_data[game_cols] = all_data.filter(regex=match_string).fillna(0)


# all_data[month + game] = all_data.filter(month + game).where(pd.notnull(all_data.filter(month + game)), all_data[game + 'OverallAvg'] * 3, axis='rows')

for month in MONTHS:
    match_string = month + 'TableNum'
    game_cols = [x for x in all_data.columns if re.match(match_string, x)]
    all_data[game_cols] = all_data.filter(regex=match_string).where(pd.notnull(all_data.filter(regex=match_string)), all_data['SatTableNum'], axis='rows')


# export to csv
all_data.to_csv('merged_data.csv')
# satTourn.to_csv('sat_data.csv', index=False)
# friTourn.to_csv('fri_data.csv', index=False)
# prezProg.to_csv('prez_data.csv', index=False)
