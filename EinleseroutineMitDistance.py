# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 16:08:49 2020

@author: helen
"""


#################### Routine zum Auslesen der Textdateien ###############################
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
def dayChoice(dropdown):
    if dropdown == "Arbeitstag - Keine Ferien":
        data = load_table_data('opti/Mo_Schule/timetable.txt')
        blockdata = load_table_data('opti/Mo_Schule/timetable-blocks.txt')
        dutydata = load_table_data('opti/Mo_Schule/timetable-duties.txt')
        return(data, dutydata, blockdata)
    elif dropdown == "Arbeitstag - Ferien":
        data = load_table_data('opti/Mo_Ferien/timetable.txt')
        blockdata = load_table_data('opti/Mo_Ferien/timetable-blocks.txt')
        dutydata = load_table_data('opti/Mo_Ferien/timetable-duties.txt')
        return(data, dutydata, blockdata)
    elif dropdown == "Samstag":
        data = load_table_data('opti/Samstag/timetable.txt')
        blockdata = load_table_data('opti/Samstag/timetable-blocks.txt')
        dutydata = load_table_data('opti/Samstag/timetable-duties.txt')
        return(data, dutydata, blockdata)
    elif dropdown == "Sonntag":
        data = load_table_data('opti/Sonntag/timetable.txt')
        blockdata = load_table_data('opti/Sonntag/timetable-blocks.txt')
        dutydata = load_table_data('opti/Sonntag/timetable-duties.txt')
        return(data, dutydata, blockdata)
data, dutydata, blockdata = dayChoice(dropdown)
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
Distance = []
count_rows_duty = dutyelements.shape[0]
count_rows_dutytype = dutytype.shape[0]
count_rows_service = servicefahrten.shape[0]
count_blocks = blocks.shape[0]
for x in range(count_rows_duty):
    for y in range(count_rows_service):
        if tableFinal.iat[x,2] == allLines.iat[y,0]:
            LineID.append(allLines.iat[y,1])
            Distance.append(allLines.iat[y,1])
    if tableFinal.iat[x,2] == -1:
            LineID.append(0)
            Distance.append(0)
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
###Routine zum HinzufÃ¼gen des Duty Typs
df_dutytype = []
for x in range(count_rows_duty):
    for y in range(count_rows_dutytype):
        if tableFinal.iat[x,0] == dutytype.iat[y,0]:
            df_dutytype.append(dutytype.iat[y,1])
tableFinal["DutyType"] = df_dutytype   
tableFinal["DepotID"] = DepotID
tableFinal["VehTypeID"] = VehTypeID
tableFinal["LineID"] = LineID
tableFinal["Distance"] = Distance
df = tableFinal

export_csv = tableFinal.to_csv(r'TESTtableFinal.csv', index=None, header=True)

