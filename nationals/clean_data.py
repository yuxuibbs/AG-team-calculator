import pandas as pd

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


satTourn = change_data('2023-2024/Clic2324.xlsx',
                        'Saturday Tournaments',
                        ['FirstName', 'LastName', 'Full Name', 'Grade',
                         'Sept', 'SeptTable', 'SeptGame',
                         'Oct', 'OctTable', 'OctGame',
                         'Nov', 'NovTable', 'NovGame',
                         'Dec', 'DecTable', 'DecGame',
                         'Jan', 'JanTable', 'JanGame',
                         'Feb', 'FebTable', 'FebGame',
                         'Total', 'Avg', 'TableAvg', 'AvgWithTableBump', 'AdjAvg'
                        ],
                        'FirstName',
                        ['Full Name', 'Total', 'Avg', 'TableAvg', 'AvgWithTableBump',
                         'AdjAvg'])

friTourn = change_data('2023-2024/Clic2324.xlsx',
                        'Team Standings',
                        ['FirstName', 'LastName', 'Grade',
                         'EQ1', 'EQ2', 'EQ3', 'EQ4', 'EQ_CM', 'EQ5',
                         'OS1', 'OS2', 'OS_CM', 'EQ_Worksheets', 'OS3', 'OS4', 'OS5',
                         'Ling1', 'Ling_CM', 'OS_Worksheets', 'Ling2', 'Ling3', 'Ling_Worksheets', 'Ling4', 'Ling5',
                         'Mixed', 'Mixed', 'Prop1', 'Pres', 'Prop2',
                         'Total', 'EQ Total', 'OS total', 'Ling total', 'WFF Total',
                         'Tour total', 'Cube Avg', 'CM', 'Wks', 'Wks Rem'
                        ],
                        'Grade',
                        ['Mixed',
                        'Total', 'EQ Total', 'OS total', 'Ling total', 'WFF Total',
                        'Tour total', 'Cube Avg', 'CM', 'Wks', 'Wks Rem']
                        )
prezProg = change_data('2023-2024/Clic2324.xlsx',
                        'Pres Prog',
                        ['FirstName', 'LastName', 'Full Name', 'Grade',
                         '6-Oct_1', '20-Oct_2',
                         '3-Nov_1', '10-Nov_2',
                         '17-Nov_1', '1-Dec_2',
                         '8-Dec_1', '22-Dec_2',
                         '26-Jan_1', '2-Feb_2',
                         '23-Feb_2',
                         'Average'
                        ],
                        'FirstName',
                        ['Full Name', 'Average'])

rankings = change_data('2023-2024/Clic2324.xlsx',
                        'Nat Qualifying All Sat+Pres',
                        ['FirstName', 'LastName', 'Full Name', 'Grade',
                         'Saturdays', 'Fridays', 'States', 'Presidents', 'Total'
                        ],
                        'FirstName',
                        ['Full Name'])

states = change_data('2023-2024/Clic2324.xlsx',
                        'States',
                        ['Team', 'FirstName', 'LastName', 'Full Name',
                         'EQ1', 'EQ2', 'EQ3', 'EQ4', 'EQ_total',
                         'OS1', 'OS2', 'OS3', 'OS4', 'OS_total',
                         'Drop',
                         'CE1', 'CE2', 'CE_total', 'Drop',
                         'Prez1', 'Prez2', 'Prez_total',
                         'Drop', 'Drop',
                         'Ling1', 'Ling2', 'Ling3', 'Ling4', 'Ling_total',
                         'Prop1', 'Prop2', 'Prop_total',
                         'Drop', 'Drop',
                         'Drop', 'Drop', 'Drop', 'Drop', 'Drop',
                         'Sweeps', 'Sweeps - Wff', '5 Game', 'TableAdjustment', 'Drop',
                         'Ling_playoff', 'EQ_playoff', 'OS_playoff', 'WFF_playoff'
                        ],
                        'FirstName',
                        ['Full Name', 'Drop'])

satTourn.to_csv('2023-2024/saturday_tournaments.csv', index=False)
friTourn.to_csv('2023-2024/friday_tournaments.csv', index=False)
prezProg.to_csv('2023-2024/prez_progression.csv', index=False)
rankings.to_csv('2023-2024/rankings.csv', index=False)
states.to_csv('2023-2024/states.csv', index=False)
