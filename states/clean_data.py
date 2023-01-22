import pandas as pd
import numpy as np

def read_input_file(input_file, sheet_name=0):
    return pd.read_excel(input_file, dtype=str, sheet_name=sheet_name)

def remove_unnecessary_rows(df, row, rows_to_remove):
    df = df[pd.notnull(df[row])]
    df = df[df['FirstName'] != '0']
    df['FirstName'] = df['FirstName'].map(lambda x: x.rstrip().rstrip('©').rstrip())
    df['LastName'] = df['LastName'].map(lambda x: x.rstrip().rstrip('©').rstrip())
    df = df.drop(rows_to_remove, axis=1)
    return df

def change_data(fileName, sheet_name, columns, key, cols_to_remove):
    data = read_input_file(fileName, sheet_name)
    data.columns = columns
    data = remove_unnecessary_rows(data, key, cols_to_remove)
    return data


satTourn = change_data('2022-2023/Clague22.xlsx', 
                        0, 
                        ['FirstName', 'LastName', 'Grade', 
                            'Sept', 'SeptTable', 'SeptGame', 
                            'Oct', 'OctTable', 'OctGame', 
                            'Nov', 'NovTable', 'NovGame', 
                            'Dec', 'DecTable', 'DecGame', 
                            'Jan', 'JanTable', 'JanGame', 
                            'Feb', 'FebTable', 'FebGame', 
                            'Total', 'Avg', 'TableAvg', 'AvgWithTableBump', 'AdjAvg'], 
                        'FirstName', 
                        ['Total', 'Avg', 'TableAvg', 'AvgWithTableBump', 'AdjAvg', "Feb", "FebTable", "FebGame"])

friTourn = change_data('2022-2023/Clic2223.xlsx',
                        'Individual Standings',
                        ['FirstName', 'LastName', 'Grade', 'Team',
                            'EQ1', 'EQ2', 'EQ3', 'EQ4', 'EQ5', 'EQ_CM', 
                            'OS1', 'OS2', 'OS3', 'EQ_Worksheets', 'OS4', 'OS_CM', 'OS5', 
                            'Ling1', 'Ling2', 'Ling3', 'OS_Worksheets', 'Ling4', 'Ling5', 'Ling_Worksheets', 
                            'Mixed', 'Mixed', 'Mixed', 'Mixed', 'Mixed', 'Mixed', 'Mixed', 
                            'Total', 'EQ Total', 'OS Total', 'Ling Total', 'WFF Total',
                            'TournamentTotal', 'Avg', 'Challenge Match', 'Worksheets', 'WorksheetsRemaining'],
                        'Grade', 
                        ['Total', 'EQ Total', 'OS Total', 'Ling Total', 'TournamentTotal', 'Avg', 'Challenge Match', 'Worksheets', 'WorksheetsRemaining', 'Mixed']
                        )
prezProg = change_data('2022-2023/PresProgression2223.xlsx',
                        'Sheet1',
                        ['FirstName', 'LastName', 'Grade', 
                            '7-Oct_1', '14-Oct_2', '21-Oct_1', 
                            '4-Nov_2', '11-Nov_1', '18-Nov_2', 
                            '2-Dec_1', '9-Dec_2', '16-Dec_1', 
                            '13-Jan_2', '20-Jan_1', 
                            'Drop', 'Drop', 'Drop', 'Drop', 'Drop', 'Drop', 'Average'],
                        'FirstName', 
                        ['Average', 'Drop'])

rankings = change_data('2022-2023/State Qualifying \'23.xlsx',
                        'All Saturdays',
                        ['FirstName', 'LastName', 'Grade', 'Saturdays', 'Fridays', 'Total', '20-Jan'],
                        'FirstName', 
                        ['20-Jan'])

satTourn.to_csv('2022-2023/saturday_tournaments.csv', index=False)
friTourn.to_csv('2022-2023/individual_rankings.csv', index=False)
prezProg.to_csv('2022-2023/prez_progression.csv', index=False)
rankings.to_csv('2022-2023/rankings.csv', index=False)

