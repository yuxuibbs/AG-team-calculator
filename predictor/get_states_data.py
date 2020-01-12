import pandas as pd
import numpy as np
import helper_functions

states = 'Clsts19.xlsx'
statesResults = helper_functions.read_input_file(states, 'Individuals').iloc[:, [0, 1, 6, 11, 17, 24, 27, 34]]
statesResults.columns = ['FirstName', 'LastName', 'EQTotal', 'OSTotal', 'PrezTotal', 'LingTotal', 'PropTotal', 'WFFTotal']
states = helper_functions.fix_names(statesResults)
states.to_csv('states_data.csv', index=False)
