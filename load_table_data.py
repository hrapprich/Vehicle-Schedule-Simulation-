import pandas as pd
import numpy as np
import sys, datetime as dt
from io import StringIO

def load_table_data(fullfilepath):

    ### Read file
    tab_dict = {}
    with open(fullfilepath) as in_file:

    	### Iterate over rows
        while True:
            try:
                curr_row = in_file.readline()
            except IOError as e:
                sys.exit(1)

            if curr_row == '':      break    ### Empty (last) row found
            if curr_row[0] == '*':  continue ### Comment found
            if curr_row[0] == '$':           ### New table found
                split_list = curr_row.split(':')
                curr_row = split_list[1]
                tab_dict[split_list[0]] = ''

            ### Append current row to table string
            tab_dict[split_list[0]] = tab_dict[split_list[0]] + curr_row
        in_file.close()

    ### Create dict of pd.DataFrames
    tab_df_dict = {}
    for name, t in tab_dict.items():
        tab_df_dict[name] = (pd.read_csv(StringIO(t), sep=';'))
    return tab_df_dict


#### Test
load_table_data('my_test_file.txt')
