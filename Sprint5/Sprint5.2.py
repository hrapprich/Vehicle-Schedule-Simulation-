"""
Damit die Daten eingelesen werden kÃ¶nnen:
Bitte speichern Sie den Ordner "opti", welcher alle Daten inkludiert, am selben Ort, an dem die Pythondatei abgespeichert ist.
Der opti Ordner muss die Unterordner "Mo_Ferien", "Mo_Schule", "Samstag" und "Sonntag" besitzen.
In den jeweiligen Ordnern mÃ¼ssen eine timetable.txt, timetable-blocks.txt und eine timetable-duties.txt Datei hinterlegt sein.

"""

#Sprint5.1

# Ã¼berall kleine Fehler im Output (Daten Schuld? DatenqualitÃ¤t Ã¼berprÃ¼fen)

# Bei DurchfÃ¼hrung Error in den Daten ausgefallen:
#   Bei VehID 9, 77, 63 sind die TeilumlÃ¤ufe nicht in korrekter Reihenfolge
#   Idee: Zeiten aufsteigend sortieren bei Transformieren

#######To-Dos########
## Prio 2: Mehrere Tage simulieren
## Prio 2: GUI optisch und inhaltlich verbessern (mehrere Dateien als AuswahlmÃ¶glichkeit)
    ## Prio 1: Stau einfÃ¼gen --> Erster Aufschlag implementiert
## Prio 1: Mehr und validere VerspÃ¤tungsarten
## Prio 1: ModularitÃ¤t ausbauen
    ## Prio 1: Dem Output die VerspÃ¤tungsart hinzufÃ¼gen --> Erster Aufschlag implementiert
    ## Prio 2: Einleseroutine hinzufÃ¼gen --> Done
## Prio 3: Dateninkonsistenzen beseitigen
## Prio 2: KPIs
## Prio 1: VerspÃ¤tungen in relative Werte wandeln (und runden)
## Prio 1: Pausenzeiten nutzen oder nicht?


## Zu klÃ¤ren:
## Statt mit absoluten VerspÃ¤tungen lieber mit relativen VerspÃ¤tungen arbeiten?
## Warum gibt es eine Haltestelle 244?


####################### Import Packages ###################################
import simpy
import pandas as pd
import numpy
from random import randint
from tkinter import *
import sys, datetime as dt
from io import StringIO

### GUI ###
root = Tk()
root.geometry("400x500")
l1 = Label(root,text='Berufsverkehr',background='grey', font = "Times")
var1 = IntVar() 
c1 = Checkbutton(root, text='An diesem Tag gibt es Berufsverkehr.', variable=var1)
l2 = Label(root,text='Wetter',background='grey', font = "Times")
var2 = IntVar() 
c2 = Checkbutton(root, text='An diesem Tag gibt es Gewitter.', variable=var2)
var3 = IntVar() 
c3 = Checkbutton(root, text='An diesem Tag regnet es.', variable=var3) 
var4 = IntVar() 
c4 = Checkbutton(root, text='An diesem Tag scheint die Sonne.', variable=var4)
l3 = Label(root,text='Tag, der simuliert wird',background='grey', font = "Times")
var5 = IntVar()
c5 = Checkbutton(root, text='Wochentag - Keine Ferien', variable=var5)  
var6 = IntVar()
c6 = Checkbutton(root, text='Wochentag - Ferien', variable=var6)  
var7 = IntVar()
c7 = Checkbutton(root, text='Samstag', variable=var7) 
var8 = IntVar() 
c8 = Checkbutton(root, text='Sonntag', variable=var8) 
button = Button(text = "BestÃ¤tigen", bg = "green", font = "Times", command = root.destroy)
 

l3.pack(fill=X, padx='20', pady='5')
c6.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
c7.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
c8.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
c5.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
l1.pack(fill=X, padx='20', pady='5')
c1.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
l2.pack(fill=X, padx='20', pady='5')
c2.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
c3.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
c4.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
button.pack(side='bottom', fill='y', padx='5',pady='10')

mainloop()


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


Weekday_No_Vacation = var5.get()
Weekday_Vacation = var6.get()
Saturday = var7.get()
Sunday = var8.get()

def dayChoice(Weekday_No_Vacation, Weekday_Vacation, Saturday, Sunday):
    if Weekday_No_Vacation == 1:
        data = load_table_data('opti/Mo_Schule/timetable.txt')
        blockdata = load_table_data('opti/Mo_Schule/timetable-blocks.txt')
        dutydata = load_table_data('opti/Mo_Schule/timetable-duties.txt')
        return(data, dutydata, blockdata)
    elif Weekday_Vacation == 1:
        data = load_table_data('opti/Mo_Ferien/timetable.txt')
        blockdata = load_table_data('opti/Mo_Ferien/timetable-blocks.txt')
        dutydata = load_table_data('opti/Mo_Ferien/timetable-duties.txt')
        return(data, dutydata, blockdata)
    elif Saturday == 1:
        data = load_table_data('opti/Samstag/timetable.txt')
        blockdata = load_table_data('opti/Samstag/timetable-blocks.txt')
        dutydata = load_table_data('opti/Samstag/timetable-duties.txt')
        return(data, dutydata, blockdata)
    elif Sunday == 1:
        data = load_table_data('opti/Sonntag/timetable.txt')
        blockdata = load_table_data('opti/Sonntag/timetable-blocks.txt')
        dutydata = load_table_data('opti/Sonntag/timetable-duties.txt')
        return(data, dutydata, blockdata)
      

data, dutydata, blockdata = dayChoice(Weekday_No_Vacation, Weekday_Vacation, Saturday, Sunday)

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

df = tableFinal
###export_csv = tableFinal.to_csv(r'TESTtableFinal.csv', index=None, header=True)


####################### Daten einlesen ####################################

#df = pd.read_csv("tableFinal.csv", sep=";")
####################### Daten transformieren und neue Zeitspalten in Dataframe einfÃ¼gen (Zeit) ########################
# Umrechnung der Start- & Endzeit in Minuten (fÃ¼r Simulationsuhr)
StartTime = []
count_row = df.shape[0]
for x in range(0, count_row):
    min_time = df.iloc[x, 5].split(":")
    minutes = int(min_time[1]) * 60
    minutes = minutes + int(min_time[2])
    StartTime.append(minutes)
EndTime = []
count_row = df.shape[0]
for x in range(0, count_row):
    min_time = df.iloc[x, 6].split(":")
    minutes = int(min_time[1]) * 60
    minutes = minutes + int(min_time[2])
    EndTime.append(minutes)
df["EndTime"] = EndTime
df["StartTime"] = StartTime


################################ Daten fÃ¼r Simulation erzeugen ##################################
# Gesamtanzahl an Fahrzeugen ermitteln
numberVeh = df["BlockID"].unique()
numberVeh = numberVeh.tolist()  # von Array in Liste formatieren
numberVeh = [elem for elem in numberVeh if elem >= 0]  # -1 entfernen
print("Die Gesamtanzahl von Fahrzeugen betrÃ¤gt %d." % len(numberVeh))

# DepotID (jedem Fahrzeug die unique DepotID zuordnen)
DepotID = []
counter = 1
for i in range(1, len(numberVeh) + 1):
    for j in range(0, df.shape[0]):
        if df.BlockID[j] == i and counter == i:
            DepotID.append(df.DepotID[j])
            counter += 1
print("Es gibt %d verschiedene Depots." %(len(set(DepotID))))
print("Jedes Fahrzeug wurde einem Depot zugeordnet: %s." % (
        len(DepotID) == len(numberVeh)))

# StartTimes der einzelnen Fahrzeuge in jedem Teilumlauf (in Dictionary gespeichert)
DepotID_plusOne = [0] + DepotID  # DepotIDListe verlÃ¤ngern, damit Schleife mit i funktioniert
startTime_dic = {}
for i in range(1, len(numberVeh) + 1):
    startTimes_Block = []
    for j in range(len(df)):
        if df.BlockID[j] == i:
            if df.FromStopID[j] == DepotID_plusOne[i]:
                startTimes_Block.append(df.StartTime[j])
    startTimes_Block = startTimes_Block + [
        1440]  # Add to every list a 1440 as last element for simulation loop (timeout)
    startTime_dic.update(
        {(i - 1): startTimes_Block})  # i-1 damit Index bei 0 anfÃ¤ngt (wichtig fÃ¼r Schleife (nachtrÃ¤gliche Ãnderung!)

StartTime_dic = startTime_dic

numTU_proF = []
for i in range(0,len(numberVeh)):
    numTU_proF.append(len(StartTime_dic[i])-1)
print("Die Fahrzeuge fahren im Schnitt %d TeilumlÃ¤ufe am Tag."
      " Das Maximum ist %d und das Minimum %d." % (sum(numTU_proF)/len(numTU_proF), max(numTU_proF), min(numTU_proF)))

# Listen von Haltestellen (from/to) (Liste mit vielen Listen)
FromStopID = []
ToStopID = []
for i in range(1, len(numberVeh) + 1):
    fromStopID_cache = []
    toStopID_cache = []
    for j in range(0, df.shape[0]):
        if df.BlockID[j] == i:
            fromStopID_one = df.FromStopID
            fromStopID_cache.append(fromStopID_one)
            toStopID_one = df.ToStopID
            toStopID_cache.append(toStopID_one)
    FromStopID.append(fromStopID_cache)
    ToStopID.append(toStopID_cache)

############ab hier Dictionaries erstellen #####################

DriveDuration_dic = {}
FromHS_dic = {}
ToHS_dic = {}
PartStartTime_dic = {}
PartEndTime_dic = {}
ElementID_dic = {}

for i in range(1, len(numberVeh) + 1):
    DifTime = []
    PartDif = []

    FromHS = []
    PartFromHS = []

    ToHS = []
    PartToHS = []

    StartTime = []
    PartStartTime = []

    EndTime = []
    PartEndTime = []

    Umlauf = []
    Teilumlauf = []

    for j in range(0, count_row):
        if df.BlockID[j] == i:

            difTime = df.EndTime[j] - df.StartTime[j]
            fromhs = df.FromStopID[j]
            tohs = df.ToStopID[j]
            stTime = df.StartTime[j]
            eTime = df.EndTime[j]
            elementID = df.ElementType[j]

            if df.ToStopID[j] == DepotID[i - 1]:
                PartDif.append(difTime)
                DifTime.append(PartDif)
                PartDif = []

                PartFromHS.append(fromhs)
                FromHS.append(PartFromHS)
                PartFromHS = []

                PartToHS.append(tohs)
                ToHS.append(PartToHS)
                PartToHS = []

                PartStartTime.append(stTime)
                StartTime.append(PartStartTime)
                PartStartTime = []

                PartEndTime.append(eTime)
                EndTime.append(PartEndTime)
                PartEndTime = []

                Teilumlauf.append(elementID)
                Umlauf.append(Teilumlauf)
                Teilumlauf = []

            else:
                PartDif.append(difTime)
                PartFromHS.append(fromhs)
                PartToHS.append(tohs)
                PartStartTime.append(stTime)
                PartEndTime.append(eTime)
                Teilumlauf.append(elementID)

    DriveDuration_dic.update({i - 1: DifTime})
    FromHS_dic.update({i - 1: FromHS})
    ToHS_dic.update({i - 1: ToHS})
    PartStartTime_dic.update({i - 1: StartTime})
    PartEndTime_dic.update({i - 1: EndTime})
    ElementID_dic.update({i - 1: Umlauf})

    ###################Art des Journeys#############################
Journey_dic = {}

for i in range(1,len(numberVeh) + 1):
    Umlauf = []
    Teilumlauf = []

    for j in range(0, count_row):
        if df.BlockID[j] == i:
            journey = df.iloc[j, 7]


            if df.ToStopID[j] == DepotID[i-1]:
                Teilumlauf.append(journey)
                Umlauf.append(Teilumlauf)
                Teilumlauf = []

            else:
                Teilumlauf.append(journey)

    Journey_dic.update({i-1: Umlauf})
    

###########Funktion um random Haltestellen auszusuchen, an denen Stau entsteht############
##Berechnet Anzahl Haltestellen
numberHS = 0
for i in range(0, count_row):
    if df.FromStopID[i] > numberHS:
        numberHS = df.FromStopID[i]
    
    
##Berechnet, welche Haltestellen am meisten frequentiert sind
HScount = []
for j in range(0, numberHS):
    count = 0
    for i in range(0, count_row):
        if df.FromStopID[i] == j:
            count += 1
    HScount.append(count)
    
##fÃ¼r die Annahme, dass ein Stau eher im Zentrum ist (Annahme, dass Zentrum dort ist, wo eine Haltestelle stark befahren wird)
cumulativeHS = []
cumulative = 0
for j in range(0, len(HScount)):
    cumulative += HScount[j]
    cumulativeHS.append(cumulative)

##Random mit gewichteter Wahrscheinlichkeit 10 Haltestellen, an denen Stau entsteht
Jam = []
for i in range(0,10):   ##Anzahl an Haltestellen mit Stau
    x = (randint(0, count_row))
    for j in range(0, len(cumulativeHS)):
        if x <= cumulativeHS[j]:
            Jam.append(j)
            break
        
############################## Funktionen fÃ¼r Objekt Vehicle #############################

# Abfrage: Fahrtzeit Ã¼ber Simulationsdauer
def drive_outOfTime(time, clock):
    doOT = time + clock > 1440
    return doOT




############################ StÃ¶rgenerator##################################
S = 5 # Einstellen des StÃ¶rfaktors

def stoerfaktor(s):  # n = Eingabeparameter um StÃ¶rausmaÃ zu steuern
    if (s == 0):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                              0.0])  # Wahrscheinlichkeiten von StÃ¶rungen / fÃ¼r jeden
        # Teilfahrt neuen StÃ¶rfaktor
    elif (s == 1):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.6, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                              0.0])  # Wahrscheinlichkeiten von StÃ¶rungen / fÃ¼r jeden
        # Teilfahrt neuen StÃ¶rfaktor
    elif (s == 2):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.6, 0.0, 0.0, 0.2, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0,
                                                              0.0])  # Wahrscheinlichkeiten von StÃ¶rungen / fÃ¼r jeden
        # Teilfahrt neuen StÃ¶rfaktor
    elif (s == 3):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.33, 0.0, 0.0, 0.0, 0.0, 0.33, 0.0, 0.0, 0.0, 0.0,
                                                              0.34])  # Wahrscheinlichkeiten von StÃ¶rungen / fÃ¼r
        # jeden Teilfahrt neuen StÃ¶rfaktor
    elif (s == 4):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0,
                                                              0.5])  # Wahrscheinlichkeiten von StÃ¶rungen / fÃ¼r
        # jeden Teilfahrt neuen StÃ¶rfaktor
    elif (s == 5):
        factorX = 20
    return factorX

##VerspÃ¤tungen auÃerhalb der Simulation bilden
"""
def verspÃ¤tung():

    for fzg in range(1,len(numberVeh) + 1):
        shift = 0
        for partNbr in range(0, len(StartTime_dic[fzg-1])-1):
            if partNbr > 0:                ##wenn es nicht der erste teilumlauf ist, kann es zu abhÃ¤ngigkeiten zw den umlÃ¤ufen kommen
                lastTime = len(PartEndTime_dic[fzg-1][partNbr-1])-1   ##Zeit des letzten Umlaufs
                ##Wenn Umlauf starten soll, obwohl letzter Umlauf noch nicht beendet:
                if PartStartTime_dic[fzg-1][partNbr][0] < PartEndTime_dic[fzg-1][partNbr-1][lastTime]:
                    shift += PartEndTime_dic[fzg-1][partNbr-1][lastTime] - PartStartTime_dic[fzg-1][partNbr][0]
                    PartStartTime_dic[fzg-1][partNbr][0] = PartEndTime_dic[fzg-1][partNbr-1][lastTime]
                ##wenn Umlauf starten soll und letzter Umlauf auch beendet ist: (Zeitverschiebung kann verringert werden)
                if PartStartTime_dic[fzg-1][partNbr][0] > PartEndTime_dic[fzg-1][partNbr-1][lastTime]:
                    shift -= PartStartTime_dic[fzg-1][partNbr][0] - PartEndTime_dic[fzg-1][partNbr-1][lastTime]
                if shift < 0:
                    shift = 0

                ##FÃ¼r jeden Teilumlauf die einzelnen Fahrten durchiterieren
            for journey in range(0, len(PartStartTime_dic[fzg-1][partNbr])):
                if journey > 0:
                    PartStartTime_dic[fzg-1][partNbr][journey] = PartEndTime_dic[fzg-1][partNbr][journey-1]
                ##Wenn es keine Standzeit ist:
                if Journey_dic[fzg-1][partNbr][journey] != 9:
                    delaytime = stoerfaktor(2) ##Hier werden die StÃ¶rfaktoren eingebaut
                    shift += delaytime
                    PartEndTime_dic[fzg-1][partNbr][journey] = PartStartTime_dic[fzg-1][partNbr][journey] + DriveDuration_dic[fzg-1][partNbr][journey] + delaytime
                ##Wenn es eine Standzeit ist:
                if Journey_dic[fzg-1][partNbr][journey] == 9:
                    ##Wenn Verschiebung grÃ¶Ãer/gleich der Pausenzeit
                    if DriveDuration_dic[fzg-1][partNbr][journey] < shift:
                        shift = shift - DriveDuration_dic[fzg-1][partNbr][journey]
                        PartEndTime_dic[fzg-1][partNbr][journey] = PartStartTime_dic[fzg-1][partNbr][journey]
                    ##Wenn Verschiebung kleiner Pausenzeit ist
                    elif DriveDuration_dic[fzg-1][partNbr][journey] >= shift:
                        if shift < 0:
                            shift = 0
                        PartEndTime_dic[fzg-1][partNbr][journey] = PartStartTime_dic[fzg-1][partNbr][journey] + DriveDuration_dic[fzg-1][partNbr][journey] - shift
                        shift = 0
                if shift < 0:
                    shift = 0
                    
verspÃ¤tung()                    

"""

def carTraffic(time):
    if var1.get() == 1:
        if (time >= 390 and time <= 510) or (time >= 1110 and time <= 1200):
            return (stoerfaktor(4))
    ##oder ggf prozentual die duration erhÃ¶ren? (30% mehr zu den stoÃzeiten?)
        else:
            return (stoerfaktor(1))
    else:
        return(stoerfaktor(0))
    
    
def weather():
     if var2.get() == 1:
        return(stoerfaktor(4))
     elif var3.get() == 1:
        return(stoerfaktor(3))
     elif var4.get() == 1:
        return(stoerfaktor(1))
     else:
        return(stoerfaktor(0))
        
        

def trafficjam(FromHS, ToHS):
    if FromHS in Jam or ToHS in Jam:
        return(stoerfaktor(4))
    else:
        return(stoerfaktor(0))


def breaktime(vehID, teilumlaufnummer, fahrtnummer, delayTime):
    if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
        DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] = \
        DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] - delayTime
        if DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] < 0:
            delayTime = abs(DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer])
            DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] = 0
        else:
            delayTime = 0
    return(delayTime)
    
    
def Type(weather, traffic, jam):
    delayType = ""
    if weather > 0:
        delayType += ("Wetter")
    if traffic > 0 and delayType == "":
        delayType += ("Verkehr")
    elif traffic > 0 and delayType != "":
        delayType += (",Verkehr")
    if jam > 0 and delayType == "":
        delayType += ("Stau")
    elif jam > 0 and delayType != "":
        delayType += (",Stau")
    else:
        delayType += ("-")
    return(delayType)

############################## Daten fÃ¼r CSV-Datei ###############################
# Header fÃ¼r CSV-Datei
print("vehID Teilumlaufnummer Standort Dep/Arr Uhrzeit(Soll) Uhrzeit(Ist) FahrtverspÃ¤tung GesamtverspÃ¤tung VerspÃ¤tungsursache",
      file=open("eventqueue5.2.csv", "a"))
########################## Objekt Vehicle #########################################
def vehicle(env, vehID):  # Eigenschaften von jedem Fahrzeug
    while True:
        delayTime = 0  # DelayTime initialisieren (gilt fÃ¼r den ganze Tag des Fahrzeugs)
        delayType = ""
        for teilumlaufnummer in range(0, len(StartTime_dic)-1):  #Loop der durch die einzelnen TeilumlÃ¤ufe fÃ¼hrt
            try:
                if StartTime_dic[vehID][teilumlaufnummer] - env.now >= 0:
                    delayTime = 0
                    delayType = ""
                    yield env.timeout(
                        StartTime_dic[vehID][teilumlaufnummer] - env.now)
                else:
                    yield env.timeout(0)
                    delayTime = env.now - StartTime_dic[vehID][teilumlaufnummer]
                    delayType = ""
                            
                umlaufstatus = 1  # Wenn Startzeit erreicht, Fahrzeug im Umlauf (umlaufstatus = 1)

                while umlaufstatus == 1:  # while Fahrzeug im Umlauf
                    for fahrtnummer in range(0, len(FromHS_dic[vehID][teilumlaufnummer])):

                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            fahrtstatus = 2
                        else:
                            fahrtstatus = 0 # 0 = Abfahrt / 1 = Ankunft / 2 = Pause

                        delayTime_perDrive = 0 #fÃ¼r PrintAusgabe hier definiert
                        print(vehID + 1, teilumlaufnummer + 1, FromHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                              fahrtstatus, PartStartTime_dic[vehID][teilumlaufnummer][fahrtnummer], env.now,
                              "-", delayTime, "-",
                              file=open("eventqueue5.2.csv", "a"))

                        # VerspÃ¤tung auf Fahrt ermitteln
                        delayType = ""
                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            delayTime_perDrive = 0
                            delayType = "-"
                        else:
                            delayWeather = weather()
                            delayCarTraffic = carTraffic(env.now)
                            delayTrafficJam = trafficjam(FromHS_dic[vehID][teilumlaufnummer][fahrtnummer], ToHS_dic[vehID][teilumlaufnummer][fahrtnummer])
                            delayTime_perDrive = delayWeather + delayCarTraffic + delayTrafficJam
                            # FÃ¼ge der Outputvariable "delayType" den Grund der VerspÃ¤tung hinzu
                            delayType = Type(delayWeather, delayCarTraffic, delayTrafficJam)
                        
                        # Aufsummieren der VerspÃ¤tungen im Teilumlauf
                        delayTime += delayTime_perDrive

                        # Abfrage, ob Fahrt auÃerhalb der Simulationszeit liegen wÃ¼rde
                        if drive_outOfTime(
                                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer], env.now):
                            yield env.timeout(1440)
                            break
                        
                        # Abfrage, ob Pausenzeit & VerspÃ¤tungszeit anpassen
                        delayTime = breaktime(vehID, teilumlaufnummer, fahrtnummer, delayTime)

                        # Timeout fÃ¼r Fahrtdauer zur nÃ¤chsten Haltestelle
                        yield (env.timeout(DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] + delayTime_perDrive))

                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            fahrtstatus = 2
                        else:
                            fahrtstatus = 1

                        # Abfrage ob Bus im Depot angekommen 
                        if ToHS_dic[vehID][teilumlaufnummer][fahrtnummer] == DepotID[vehID]:
                            print(vehID + 1, teilumlaufnummer + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  fahrtstatus, PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  env.now, delayTime_perDrive, delayTime, delayType,
                                  file=open("eventqueue5.2.csv", "a"))
                            umlaufstatus = 0
                        else:
                            print(vehID + 1, teilumlaufnummer + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  fahrtstatus, PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  env.now, delayTime_perDrive, delayTime, delayType,
                                  file=open("eventqueue5.2.csv", "a"))

            except:
                if env.now >= 1440: # to avoid RunTimeError: GeneratorExit
                    return False
                continue

            ########################## Simulationsumgebung ##############################


env = simpy.Environment()

# Initialisierung von Fahrzeugen
for i in range(0,len(numberVeh)):  # Anzahl von Fahrzeugen = len(numberVeh)
    env.process(vehicle(env, i))  # Inputdaten Eigenschaften Fahrzeugen
# Simulation starten und Laufzeit festlegen
env.run(until=1440)  # Ein Tag simulieren: in Minuten ausdrÃ¼cken. 24h = 1440min
