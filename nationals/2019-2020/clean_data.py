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


satTourn = change_data('Clague 19.xlsx', 
                        0, 
                        ['FirstName', 'LastName', 'Grade', 'Sept', 'SeptTable', 'SeptGame', 'Oct', 'OctTable', 'OctGame', 'Nov', 'NovTable', 'NovGame', 'Dec', 'DecTable', 'DecGame', 'Jan', 'JanTable', 'JanGame', 'Feb', 'FebTable', 'FebGame', 'Total', 'Avg', 'TableAvg', 'AvgWithTableBump', 'AdjAvg'], 
                        'FirstName', 
                        ['Total', 'Avg', 'TableAvg', 'AvgWithTableBump', 'AdjAvg', "Feb", "FebTable", "FebGame"])

friTourn = change_data('Clic1920.xlsx',
                        'Individual Standings',
                        ['FirstName', 'LastName', 'Grade', 'Team', 'EQ1', 'EQ2', 'EQ3', 'EQ4', 'EQ_CM', 'EQ5', 'OS1', 'OS2', 'OS3', 'OS4', 'OS5', 'Ling1', 'EQ_Worksheets', 'OS_CM', 'Ling2', 'Ling_CM', 'Ling3', 'Ling4', 'OS_Worksheets', 'Ling5', 'Ling_Worksheets', 'Mixed', 'Mixed', 'Mixed', 'Mixed', 'Prop', 'Pres', 'Prop', 'Total', 'EQTotal', 'OSTotal', 'LingTotal', 'PropTotal', 'PresTotal', 'TournamentTotal', 'Avg', 'Challenge Match', 'Worksheets', 'WorksheetsRemaining', 'Mixed', 'Mixed'],
                        'Grade', 
                        ['Total', 'EQTotal', 'OSTotal', 'LingTotal', 'PropTotal', 'PresTotal', 'TournamentTotal', 'Avg', 'Challenge Match', 'Worksheets', 'WorksheetsRemaining', 'Mixed']
                        )
prezProg = change_data('Pres Progression1920.xlsx',
                        'Sheet1',
                        ['FirstName', 'LastName', 'Grade', "27-Sep_1", "4-Oct_2", "11-Oct_1", "18-Oct_2", "25-Oct_1", "1-Nov_2", "8-Nov_1", "15-Nov_2", "6-Dec_1", "13-Dec_2", "20-Dec_1", "10-Jan_2", "17-Jan", "24-Jan", 'Total'],
                        'FirstName', 
                        ['Total', "17-Jan", '24-Jan'])

rankings = change_data('Nat Qualifying \'20.xlsx',
                        'All Saturdays',
                        ['FirstName', 'LastName', 'Grade', 'Saturdays', 'Fridays', "States", 'Total', '6-Mar', '6-Mar'],
                        'States', 
                        ['6-Mar'])

states = change_data('Clsts20.xlsx',
                        'Individuals',
                        ["FirstName","LastName","Grade", "EQ1","EQ2","EQ3","EQ4","DROP","OS1","OS2","OS3","OS4","DROP","DROP","DROP","DROP","Prez1","Prez2","DROP","DROP","DROP","Ling1","Ling2","Ling3","Ling4","DROP","Prop1","Prop2","DROP","DROP","DROP","Wff1","Wff2","Wff3","Wff4","DROP","DROP","DROP","DROP","TableAdjustment","DROP","Team"],
                        'TableAdjustment', 
                        ['DROP'])

satTourn.to_csv('saturday_tournaments.csv', index=False)
friTourn.to_csv('friday_tournaments.csv', index=False)
prezProg.to_csv('prez_progression.csv', index=False)
rankings.to_csv('rankings.csv', index=False)
states.to_csv('states.csv', index=False)

