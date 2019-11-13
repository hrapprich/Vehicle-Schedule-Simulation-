# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:24:20 2019

@author: svenr
"""

import pandas as pd
import numpy as np
import sys, datetime as dt
from io import StringIO
import simpy



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

    tab_df_dict = {}
    for name, t in tab_dict.items():
        tab_df_dict[name] = (pd.read_csv(StringIO(t), sep=';'))
    return tab_df_dict


data = load_table_data('timetable.txt')
blockdata = load_table_data('timetable-blocks.txt')
dutydata = load_table_data('timetable-duties.txt')

#bestimmte Dataframes extrahieren
servicefahrten = data["$SERVICEJOURNEY"]
dutyelements = dutydata["$DUTYELEMENT"]
blockelements = blockdata["$BLOCKELEMENT"]
blocks = blockdata["$BLOCK"]
dutytype = dutydata["$DUTY"]

allBlocks = blockelements  
tableFinal = dutyelements
allLines = servicefahrten

###Routine zum Hinzufügen der VehTypeID & DepotID
VehTypeID = []
DepotID = []
for x in range(3787):
    if tableFinal.iat[x,1] == -1:
        VehTypeID.append(tableFinal.iat[(x+1),1])
        DepotID.append(tableFinal.iat[x,4])
    else:
        for y in range(100):
            if tableFinal.iat[x,1] == blocks.iat[y,0]:
                VehTypeID.append(blocks.iat[y,1])
                DepotID.append(blocks.iat[y,2])

tableFinal["DepotID"] = DepotID
tableFinal["VehTypeID"] = VehTypeID

###Routine zum Hinzufügen des Duty Typs
df_dutytype = []
for x in range(3787):
    for y in range(178):
        if tableFinal.iat[x,0] == dutytype.iat[y,0]:
            df_dutytype.append(dutytype.iat[y,1])


tableFinal["DutyType"]  = df_dutytype 
tableFinal["DepotID"] = DepotID
tableFinal["VehTypeID"] = VehTypeID

##Routine zum Hinzufügen der LinieID + entfernen überflüssiger Spalten

tableFinal = tableFinal.drop(['ServiceJourneyCode', 'TransferType', 'GroupTransferIndex', 'DeadRunTransferBlockID', 'DeadRunTransferDutyID'], axis=1)
LineID = []

for x in range(3787):
    for y in range(1461):
        if tableFinal.iat[x,2] == allLines.iat[y,0]:
            LineID.append(allLines.iat[y,1])
    if tableFinal.iat[x,2] == -1:
            LineID.append(0)

tableFinal["LineID"] = LineID

### Umrechnung der Fahrzeiten in Minuten

StartTime = []
count_row = tableFinal.shape[0]
for x in range(0, count_row):
    min_time = tableFinal.iloc[x,5].split(":")
    minutes = int(min_time[1]) * 60
    minutes = minutes + int(min_time[2])
    StartTime.append(minutes)

EndTime = []
count_row = tableFinal.shape[0]
for x in range(0, count_row):
    min_time = tableFinal.iloc[x,6].split(":")
    minutes = int(min_time[1]) * 60
    minutes = minutes + int(min_time[2])
    EndTime.append(minutes)


tableFinal["EndTime"] = EndTime
tableFinal["StartTime"] = StartTime

DifTime = []
count_row = tableFinal.shape[0]
for x in range(0, count_row):
    difTime = tableFinal.iloc[x,12] - tableFinal.iloc[x,13]
    DifTime.append(difTime)

tableFinal["Duration"] = DifTime


### Schaffung Variable für die Verspätung

DelayedStartTime = []
DelayedEndTime = []
for x in range(0, count_row):
    DelayedStartTime.append(0)
    DelayedEndTime.append(0)
tableFinal["DelayedStartTime"] = DelayedStartTime
tableFinal["DelayedEndTime"] = DelayedEndTime

count_row = tableFinal.shape[0]

def Störungsfaktor(y):
    for x in range(0, count_row):
        tableFinal.iloc[x,14] = tableFinal.iloc[x,13] * y
        tableFinal.iloc[x,15] = tableFinal.iloc[x,12] * y


def imUmlauf(x):
    if tableFinal.iloc[x,7] == 1:
        return 1
    else:
        return 0

def imDepot(x):
    if imUmlauf(x) == 1:
        return 0
    else:
        return 1

def OnTime(x):
    for x in range(0, count_row):
        if (tableFinal.iloc[x,13] - tableFinal.iloc[x,14]) == 0:
            return("in time")
        else:
            return("not in time")
    

def DelayInMinutes(x):
    for x in range(0, count_row):
        return (tableFinal.iloc[x,13] - tableFinal.iloc[x,14])

    
def Fahrzeug(x):
        return tableFinal.iloc[x,1]


def time(env):
    cur_time = 0
    Störungsfaktor(1)
    while True:
         for x in range(0, count_row):
             if tableFinal.iloc[x,13] >= cur_time and (tableFinal.iloc[x,13]-2) < (cur_time):
                 print("Vehicle: %d starts event at %s. It is %s and has a delay of %d minutes" % (Fahrzeug(x), tableFinal.iloc[x,5], OnTime(x), DelayInMinutes(x)))
         duration = 2
         cur_time = cur_time + duration
         yield env.timeout(duration)


env = simpy.Environment()
env.process(time(env))
env.run(until=720)
