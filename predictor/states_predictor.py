import pandas as pd
import numpy as np

def read_input_file(input_file, sheet_name=0):
    df = pd.read_excel(input_file, dtype=str, sheet_name=sheet_name)
    return df

def remove_unnecessary_rows(df, row, rows_to_remove):
    df = df[pd.notnull(df[row])]
    df = df[df['FirstName'] != '0']
    df['FirstName'] = df['FirstName'].map(lambda x: x.rstrip().rstrip('©').rstrip())
    df['LastName'] = df['LastName'].map(lambda x: x.rstrip().rstrip('©').rstrip())
    df = df.drop(rows_to_remove, axis=1)
    return df

def fix_names(df):
    df['Name'] = df.apply(lambda x: '%s %s' % (x['FirstName'], x['LastName']), axis=1)
    df['FirstName'] = df['Name']
    df.rename(columns={'FirstName':'FullName'}, inplace=True)
    df = df.drop(['Name', 'LastName'], axis=1)
    return df

def change_data(fileName, sheet_name, columns, key, rows_to_remove):
	pass

SaturdayTournaments = 'Clague 18.xlsx'
satTourn = read_input_file(SaturdayTournaments)
satTourn.columns = ['FirstName', 'LastName', 'Grade', 'Sept', 'SeptTableNum', 'SeptGame', 'Oct', 'OctTableNum', 'OctGame', 'Nov', 'NovTableNum', 'NovGame', 'Dec', 'DecTableNum', 'DecGame', 'Jan', 'JanTableNum', 'JanGame', 'Feb', 'FebTableNum', 'FebGame', 'Total', 'Avg', 'TableAvg', 'AvgWithTableBump', 'AdjAvg']
satTourn = remove_unnecessary_rows(satTourn, 'FirstName', ['Total', 'Avg', 'TableAvg', 'AvgWithTableBump', 'AdjAvg'])
satTourn = fix_names(satTourn)

FridayTournaments = 'Clic1819.xlsx'
friTourn = read_input_file(FridayTournaments, 'Individual Standings')
friTourn.columns = ['FirstName', 'LastName', 'Grade', 'Team', 'EQ1', 'EQ2', 'EQ3', 'EQ4', 'EQ_CM', 'EQ5', 'OS1', 'OS2', 'OS3', 'OS4', 'OS_CM', 'OS5', 'EQ_Worksheets', 'Ling1', 'Ling2', 'Ling_CM', 'Ling3', 'OS_Worksheets', 'Ling4', 'Ling5', 'Ling_Worksheets', 'Mixed', 'Mixed', 'Mixed', 'Mixed', 'Mixed', 'Mixed', 'Total', 'EQTotal', 'OSTotal', 'LingTotal', 'PropTotal', 'PresTotal', 'TournamentTotal', 'Avg', 'Challenge Match', 'Worksheets', 'WorksheetsRemaining', 'Mixed', 'Mixed']
friTourn = remove_unnecessary_rows(friTourn, 'Grade', ['Total', 'EQTotal', 'OSTotal', 'LingTotal', 'PropTotal', 'PresTotal', 'TournamentTotal', 'Avg', 'Challenge Match', 'Worksheets', 'WorksheetsRemaining', 'Mixed'])
friTourn = fix_names(friTourn)

PrezProgression = "Pres Progression1819.xlsx"
prezProg = read_input_file(PrezProgression, 'Sheet1')
prezProg.columns = ['FirstName', 'LastName', 'Grade', '28-Sep_1', '5-Oct_2', '12-Oct_1', '26-Oct_1', '2-Nov_2', '9-Nov_1', '16-Nov_2', '30-Nov_1', '14-Dec_2', '21-Dec_1', '11-Jan_2', '1-Feb_1', '8-Feb_2', '22-Feb_1', 'Total']
prezProg = remove_unnecessary_rows(prezProg, 'FirstName', ['Total'])
prezProg = fix_names(prezProg)

all_data = satTourn.set_index('FullName').join(friTourn.set_index('FullName'), lsuffix='Grade').join(prezProg.set_index('FullName'), lsuffix='GradeGrade')

all_data = all_data.drop(["Feb", "FebTableNum", "FebGame", "GradeGrade", "GradeGradeGrade", "1-Feb_1", "8-Feb_2", "22-Feb_1"], axis=1)

all_data.to_csv('merged_data.csv')
all_data[all_data['Grade'] == '6'].to_csv('elem_merged_data.csv')
all_data[all_data['Grade'] != '6'].to_csv('middle_merged_data.csv')