import pandas as pd
import dataframe_image as dfi

matches = pd.read_csv('2023-2024/Matches 2324 - Combined no WFF.csv')
matches['Name'] = matches['First Name'] + ' ' + matches['Last Name']
matches.drop(['First Name', 'Last Name'], axis=1, inplace=True)

def highlight_score(value):
    if value == 6:
        return 'background: green'
    elif value == 5:
        return 'background: yellowgreen'
    elif value == 4:
        return 'background: orange'
    elif value == 3:
        return 'background: salmon'
    else:
        return 'background: red'

def highlight_name(name, searched_name):
    return ['background: lightblue' if n.lower() == searched_name.lower() else '' for n in name]

def get_individual_game_results(df, name):
    games_played = df[df['Name'] == name]
    return games_played.reset_index(drop=True).style.map(highlight_score, subset=['Score'])

def get_matches(df, name):
    columns_for_single_match = ['Number', 'Tournament', 'Game', 'Table']
    games_played = df[df['Name'] == name]
    games = games_played[columns_for_single_match]
    result = pd.DataFrame()
    for _, row in games.iterrows():
        result = pd.concat([result, df[
            (df['Number'] == row['Number']) &
            (df['Tournament'] == row['Tournament']) &
            (df['Game'] == row['Game']) &
            (df['Table'] == row['Table'])
        ]])
    result['temp_order'] = 1
    result.loc[result['Name'] == name, 'temp_order'] = 0
    result.sort_values(['Number', 'temp_order'], inplace=True)
    result.drop('temp_order', axis=1, inplace=True)
    return result.reset_index(drop=True)\
        .style.map(highlight_score, subset=['Score'])\
        .apply(lambda x: highlight_name(x, name), subset=['Name'])

for name in matches['Name'].drop_duplicates():
    dfi.export(get_matches(matches, name).hide(axis='index'), f"2023-2024/raw_charts/{name.replace(' ', '')}_all.png")
    dfi.export(get_individual_game_results(matches, name).hide(axis='index'), f"2023-2024/raw_charts/{name.replace(' ', '')}_individual.png")
