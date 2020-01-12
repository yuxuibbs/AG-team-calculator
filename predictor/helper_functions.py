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

def fix_names(df):
    df['Name'] = df.apply(lambda x: '%s %s' % (x['FirstName'], x['LastName']), axis=1)
    df['FirstName'] = df['Name']
    df.rename(columns={'FirstName':'FullName'}, inplace=True)
    df = df.drop(['Name', 'LastName'], axis=1)
    return df
