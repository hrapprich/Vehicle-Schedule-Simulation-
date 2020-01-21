# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 11:52:35 2020

Damit die Daten eingelesen werden können:
Bitte speichern Sie den Ordner "opti", welcher alle Daten inkludiert, am selben Ort, an dem die Pythondatei abgespeichert ist.
Der opti Ordner muss die Unterordner "Mo_Ferien", "Mo_Schule", "Samstag" und "Sonntag" besitzen.
In den jeweiligen Ordnern müssen eine timetable.txt, timetable-blocks.txt und eine timetable-duties.txt Datei hinterlegt sein.
"""

import simpy
import pandas as pd
import numpy as np
from random import randint
from tkinter import *
import sys, datetime as dt
from io import StringIO



###Routine zum Auslesen der Textdateien
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


##MoSchule

data = load_table_data('opti/Mo_Schule/timetable.txt')
blockdata = load_table_data('opti/Mo_Schule/timetable-blocks.txt')
dutydata = load_table_data('opti/Mo_Schule/timetable-duties.txt')

##MoFerien
"""
data = load_table_data('opti/Mo_Ferien/timetable.txt')
blockdata = load_table_data('opti/Mo_Ferien/timetable-blocks.txt')
dutydata = load_table_data('opti/Mo_Ferien/timetable-duties.txt')
"""
##Samstag
"""
data = load_table_data('opti/Samstag/timetable.txt')
blockdata = load_table_data('opti/Samstag/timetable-blocks.txt')
dutydata = load_table_data('opti/Samstag/timetable-duties.txt')
"""
##Sonntag
"""
data = load_table_data('opti/Sonntag/timetable.txt')
blockdata = load_table_data('opti/Sonntag/timetable-blocks.txt')
dutydata = load_table_data('opti/Sonntag/timetable-duties.txt')
"""     


#relevante Dataframes extrahieren
servicefahrten = data["$SERVICEJOURNEY"]
dutyelements = dutydata["$DUTYELEMENT"]
blocks = blockdata["$BLOCK"]
blockelements = blockdata["$BLOCKELEMENT"]
dutytype = dutydata["$DUTY"]      

allBlocks = blockelements  
tableFinal = dutyelements
allLines = servicefahrten

tableFinal = tableFinal.drop(['ServiceJourneyCode', 'TransferType', 'GroupTransferIndex', 'DeadRunTransferBlockID', 'DeadRunTransferDutyID'], axis=1)
LineID = []

count_rows_duty = dutyelements.shape[0]
count_rows_dutytype = dutytype.shape[0]
count_rows_service = servicefahrten.shape[0]
count_blocks = blocks.shape[0]

for x in range(count_rows_duty):
    for y in range(count_rows_service):
        if tableFinal.iat[x,2] == allLines.iat[y,0]:
            LineID.append(allLines.iat[y,1])
    if tableFinal.iat[x,2] == -1:
            LineID.append(0)


VehTypeID = []
DepotID = []
for x in range(count_rows_duty):
    if tableFinal.iat[x,1] == -1:
        VehTypeID.append(tableFinal.iat[(x+1),1])
        DepotID.append(tableFinal.iat[x,4])
    else:
        for y in range(count_blocks):
            if tableFinal.iat[x,1] == blocks.iat[y,0]:
                VehTypeID.append(blocks.iat[y,1])
                DepotID.append(blocks.iat[y,2])


###Routine zum Hinzufügen des Duty Typs
df_dutytype = []
for x in range(count_rows_duty):
    for y in range(count_rows_dutytype):
        if tableFinal.iat[x,0] == dutytype.iat[y,0]:
            df_dutytype.append(dutytype.iat[y,1])
  
tableFinal["DutyType"] = df_dutytype   
tableFinal["DepotID"] = DepotID
tableFinal["VehTypeID"] = VehTypeID
tableFinal["LineID"] = LineID

export_csv = tableFinal.to_csv(r'tableFinalNEW.csv', index=None, header=True)
