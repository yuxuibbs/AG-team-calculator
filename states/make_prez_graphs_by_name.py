import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
import numpy as np

prezProg = pd.read_csv('2023-2024/prez_progression.csv')

all_prez = ['6-Oct_1', '20-Oct_2', '3-Nov_1', '10-Nov_2', '17-Nov_1', '1-Dec_2', '8-Dec_1', '22-Dec_2']
first_half = ['6-Oct_1', '3-Nov_1', '17-Nov_1', '8-Dec_1']
second_half = ['20-Oct_2', '10-Nov_2', '1-Dec_2', '22-Dec_2']

all_prez_color = 'black'
first_half_color = 'blue'
second_half_color = 'red'

def get_line_best_fit(data):
    if len(data) > 1:
        coefficients = np.polyfit(range(len(data)), data, 1)
        line_of_best_fit = np.polyval(coefficients, range(len(data)))
        return [coefficients, line_of_best_fit]
    else:
        return [[0], 0]

def make_graph(row, name):
    # get columns
    all_prez_cols = sorted(list(set(row.keys()).intersection(all_prez)), key=lambda x: all_prez.index(x))
    first_half_cols = sorted(list(set(row.keys()).intersection(first_half)), key=lambda x: all_prez.index(x))
    second_half_cols = sorted(list(set(row.keys()).intersection(second_half)), key=lambda x: all_prez.index(x))
    # get data
    all_prez_data = [int(x) for x in row[all_prez_cols]]
    first_half_data = [int(x) for x in row[first_half_cols]]
    second_half_data = [int(x) for x in row[second_half_cols]]

    # make graphs
    fig, ax = plt.subplots(1, 1, figsize=(16, 9))

    # all prez
    if all_prez_cols:
        ax.plot(all_prez_cols, all_prez_data, label='All', color=all_prez_color)
        # line of best fit
        [coefficients, line_of_best_fit] = get_line_best_fit(all_prez_data)
        ax.plot(all_prez_cols, line_of_best_fit, color=all_prez_color, label=f'All {coefficients[0]}')

    # first half
    if first_half_cols:
        ax.scatter(first_half_cols, first_half_data, label='16-24', color=first_half_color)
        # line of best fit
        [coefficients, line_of_best_fit] = get_line_best_fit(first_half_data)
        ax.plot(first_half_cols, line_of_best_fit, color=first_half_color, label=f'16-24 {coefficients[0]}')

    # second half
    if second_half_cols:
        ax.scatter(second_half_cols, second_half_data, label='25-33', color=second_half_color)
        # line of best fit
        [coefficients, line_of_best_fit] = get_line_best_fit(second_half_data)
        ax.plot(second_half_cols, line_of_best_fit, color=second_half_color, label=f'25-33 {coefficients[0]}')


    ax.set_title(name)
    ax.set_ylim([-1, 32])
    ax.legend()

    return fig

def highlight_half(df):
    df_colors = pd.DataFrame(index=df.index, columns=df.columns)
    df_colors.iloc[df['Variable_Name'].isin(first_half), :] = f'background: {first_half_color}; color: white;'
    df_colors.iloc[df['Variable_Name'].isin(second_half), :] = f'background: {second_half_color}; color: white;'
    return df_colors

def make_chart(df):
    output = df.reset_index()
    output.columns = ['Variable_Name', 'Score']
    return output


for _, row in prezProg.iterrows():
    name = row['FirstName'] + ' ' + row['LastName']
    plt.close(make_graph(row.dropna(), name).savefig(f"2023-2024/raw_charts/{name.replace(' ', '')}_prez.png", bbox_inches='tight'))
    dfi.export(make_chart(pd.DataFrame(row)).style.apply(highlight_half, axis=None).hide(axis='index'), f"2023-2024/raw_charts/{name.replace(' ', '')}_prez_data.png")
