# -*- coding: utf-8 -*-
"""
pip install ttk themes

Damit das Tool genutzt werden kann:
Zunächst muss simpy installiert werden. Dafür im cmd den Befehl "pip install simpy" ausführen.
Damit die Daten eingelesen werden können:
Bitte speichern Sie den Ordner "opti", welcher alle Daten inkludiert, am selben Ort, an dem die Pythondatei abgespeichert ist.
Der opti Ordner muss die Unterordner "Mo_Ferien", "Mo_Schule", "Samstag" und "Sonntag" besitzen.
In den jeweiligen Ordnern müssen eine timetable.txt, timetable-blocks.txt und eine timetable-duties.txt Datei hinterlegt sein.
"""
"""
Aus Testzwecken macht es momentan keinen Unterschied welchen Datensatz man in der GUI auswählt. 
Es wird momentan immer der Datensatz Montag-Freitag keine Ferien verwendet.
Auch das Eingabefeld und der Regler sind momentan nicht mit dem Code verknüpft.
"""

####################### Import Packages ###################################
import simpy
import pandas as pd
import numpy
import random
from random import randint
from tkinter import *
from tkinter import font
import tkinter.ttk as ttk 


###################### Interface Störungen ####################################
# Ausmaß = Anteil an Fahrten, die von der Störung betroffen sind
# Delay = Verspätung (relativ zur Fahrtdauer der Fahrt), die zur Fahrtdauer hinzukommt

## neue Variablen
#Rushhour-Funktion
RushhourStart1 = 390
RushhourEnde1 = 510
RushhourStart2 = 870
RushhourEnde2 = 1110
delayRushhour = 2
#Event-Veranstaktungen
#eventOrte = [39]

#Ab zeile 593 kann man die weiteren Funktionen aktivieren (müssten dann später in die GUI)
'''
# rdmStau-Funktion
anzahlStaus = 20 # pro Simulationstag
staudauerMin = 10 # wie lange hält der Stau mindestens an (in Minuten)
staudauerMax = 50 # wie lange hält der Stau maximal an (in Minuten)
delayStau = 0.5 # Fahrtdauer verlängert sich bei Stau um 50%
'''
# Sturm
ausmaßSturm = 0.8 # 80 % der Fahrten sind von Störung betroffen
delaySturm = 0.4 # Fahrtdauer verlänget sich Sturm um 60%
# Regen
ausmaßRegen = 0.5 # 50 % der Fahrten sind von Störung betroffen
delayRegen = 0.1 # Fahrtdauer verlänget sich Sturm um 40%
# Fahrzeugausfall
ausmaßAusfall = 0.01 # 1% Wahrscheinlichkeit, dass Fahrzeug ausfällt (delay = 1440)
# Baustelle an bestimmten Haltestellen
delayBaustelle = 1 # Fahrtdauer bei Baustelle verdoppelt sich
# Unfall
ausmaßUnfall = 0.05 # 5% Wahrscheinlichkeit, dass Unfall während der Fahrt passiert (Fahrzeug nicht beteiligt)
delayUnfall = round(random.uniform(0.5,2),2) # Fahrtdauer bei Unfall variiert zwischen 0.5 & 2

delayEvent = 12 # absolute Zahl
delayBaustelle = 10 #absolute Zahl
######################## GUI Design #############################################


root = Tk()
s=ttk.Style()
s.theme_use('clam')
##Wählbare Themes:'winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'

root.resizable(width=False, height= False)
#root.iconbitmap('favicon.ico')
root.geometry('+0+0')
root.title('Simulationstool zur Überprüfung der Robustheit von Fahrzeugeinsatzplänen')
s.configure('TButton', background='green', padding=(50, 10), font=('Verdana', 10, 'bold'))
Überschrift = font.Font(family='Verdana', size=11, weight='bold')
Überschrift2 = font.Font(family='Verdana', size=10, weight='bold')
Text= font.Font(family="Verdana", size=9)
Bestätigung= font.Font(family="Verdana", size=11, weight="bold")

#1 Eingabefelder anlegen und positionieren
Frame0 = Frame(root, bg = "grey", padx=6, pady=6)
Frame0.grid(row=0, columnspan = 8)
Frame1 = Frame(root, bg = "grey", padx=6, pady=6)
Frame1.grid(row=5, columnspan = 8)
Frame2 = Frame(root, bg = "grey", padx=6, pady=6)
Frame2.grid(row=12, columnspan = 8)

label0 = Label(Frame0, text="Einstellungen", width = 50, height = 1, bg = "grey", font = Überschrift).grid(row=0)
label1 = Label(Frame1, text="Globale Störungsmuster", width = 50, height = 1, bg = "grey", font = Überschrift).grid(row=5)
label2 = Label(Frame2, text="Selektive Störungsmuster", width = 50, height = 1, bg = "grey", font = Überschrift).grid(row=11)
label4 = Label(text="Wetter", width = 20, height = 1, bg = "darkgrey", font = Überschrift2).grid(row=6, column = 2)
label5 = Label(text="Fahrerausfall", width = 20, height = 1, bg = "indian red", font = Überschrift2).grid(row=9, column = 2)
label6 = Label(text="Defekt", width = 20, height = 1, bg = "indian red", font = Überschrift2).grid(row=6, column = 5)
label7 = Label(text="Veranstaltung", width = 20, height = 1, bg = "darkgrey", font = Überschrift2).grid(row=13, column = 2)
label8 = Label(text="Unfall", width = 20, height = 1, bg = "indian red", font = Überschrift2).grid(row=15, column = 2)
label9 = Label(text="Baustelle", width = 20, height = 1, bg = "darkgrey", font = Überschrift2).grid(row=17, column = 2)
label10 = Label(text="Sonstige Streiks", width = 20, height = 1, bg = "indian red", font = Überschrift2).grid(row=19, column = 2)
label11 = Label(text="Defekt", width = 20, height = 1, bg = "indian red", font = Überschrift2).grid(row=22, column = 2)


button = ttk.Button(text = "Bestätigen", style = 'TButton', command = root.destroy)
button.grid(row = 25, column = 0, columnspan=5, sticky = S+W)

##############Dropdown##############


chosenDay = StringVar()
day = ttk.Combobox(root, textvariable = chosenDay)
day['values'] = ["Wochentag - Keine Ferien", "Wochentag Ferien", "Samstag", "Sonntag"]
day.grid(row = 2, column = 5, sticky=W)
day.current(0)

varPufferzeit = StringVar()
pufferzeit = ttk.Combobox(root, textvariable = varPufferzeit)
pufferzeit['values'] = ["Ja", "Nein"]
pufferzeit.grid(row = 4, column = 5, sticky=W)
pufferzeit.current(0)

####################################
Label(root, text="  Folgender Wochentag soll", font = Text).grid(row=1, column = 2, columnspan = 7, sticky = W)
Label(root, text="  simuliert werden:", font = Text).grid(row=2, column = 2, columnspan = 7, sticky = W)
Label(root, text="  Sollte Pufferzeit zum Abbau von", font = Text).grid(row=3, column = 2, columnspan = 7, sticky = W)
Label(root, text="  Verspätungen genutzt werden?", font = Text).grid(row=4, column = 2, columnspan = 7, sticky = W)
varKrankheit = IntVar()
Checkbutton7 = Checkbutton(root, text = "Krankheit", font = Text, variable = varKrankheit)
Checkbutton7.grid(row = 10, column = 2, columnspan=7, sticky=W)

varStreik = IntVar()
Checkbutton8 = Checkbutton(root, text = "Streik des ÖPNV", font = Text, variable = varStreik)
Checkbutton8.grid(row = 11, column = 2, columnspan=7, sticky=W)

varSturm = IntVar()
Checkbutton9 = Checkbutton(root, text = "Sturm", font = Text, variable = varSturm)
Checkbutton9.grid(row = 7, column = 2, columnspan=7, sticky=W)

varRegen = IntVar()
Checkbutton10 = Checkbutton(root, text = "Regen", font = Text, variable = varRegen)
Checkbutton10.grid(row = 8, column = 2, columnspan=7, sticky=W)

varDefekt = IntVar()
Checkbutton11 = Checkbutton(root, text = "Fahrzeugdefekt im Depot", font = Text, variable = varDefekt)
Checkbutton11.grid(row = 7, column = 5, columnspan=7, sticky=W)

label12 = Label(root, text="  Veranstaltung nahe der Haltestelle:", font = Text).grid(row=14, column = 2, columnspan = 7, sticky = W)
varVeranstaltung = StringVar()
Entry(root,textvariable=varVeranstaltung).grid(row=14, column=5, sticky = W)

label13 = Label(root, text="  Unfall nahe der Haltestelle:", font = Text).grid(row=16, column = 2, columnspan = 7, sticky = W)
varUnfall = StringVar()
Entry(root,textvariable=varUnfall).grid(row=16, column=5, sticky = W)

label14 = Label(root, text="  Baustelle nahe der Haltestelle:", font = Text).grid(row=18, column = 2, columnspan = 7, sticky = W)
varBaustelle = StringVar()
Entry(root,textvariable=varBaustelle).grid(row=18, column=5, sticky = W)

label15 = Label(root, text="  Straßensperrungen nahe der:", font = Text).grid(row=20, column = 2, columnspan = 7, sticky = W)
label16 = Label(root, text="  Haltestelle:", font = Text).grid(row=21, column = 2, columnspan = 7, sticky = W)
varSperrung = StringVar()
Entry(root,textvariable=varSperrung).grid(row=21, column=5, sticky = W)

label17 = Label(root, text="  Fahrzeugdefekt während der", font = Text).grid(row=23, column = 2, columnspan = 7, sticky = W)
label18 = Label(root, text="  Fahrt nahe der Haltestelle:", font = Text).grid(row=24, column = 2, columnspan = 7, sticky = W)
varDefekt = StringVar()
Entry(root,textvariable=varDefekt).grid(row=24, column=5, sticky = W)

root.mainloop()


if varVeranstaltung.get() != (""):
    eventOrte = varVeranstaltung.get().split(', ')
    for i in range(len(eventOrte)):
        eventOrte[i] = int(eventOrte[i])
else:
    eventOrte = []
    
if varUnfall.get() != (""):
    varUnfall = varUnfall.get().split(', ')
    for i in range(len(varUnfall)):
        varUnfall[i] = int(varUnfall[i])
else:
    varUnfall = []        

if varBaustelle.get() != (""):
    BaustellenListe = varBaustelle.get().split(', ')
    for i in range(len(BaustellenListe)):
        BaustellenListe[i] = int(BaustellenListe[i])
else:
    BaustellenListe = []

if varSperrung.get() != (""):
    varSperrung = varSperrung.get().split(', ')
    for i in range(len(varSperrung)):
        varSperrung[i] = int(varSperrung[i])
else:
    varSperrung = []
    
if varDefekt.get() != (""):
    varDefekt = varDefekt.get().split(', ')
    for i in range(len(varDefekt)):
        varDefekt[i] = int(varDefekt[i])
else:
    varDefekt = []

if varPufferzeit.get() == "Ja":
    varPufferzeit = 1
else:
    varPufferzeit = 0


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
"""
###export_csv = tableFinal.to_csv(r'TESTtableFinal.csv', index=None, header=True)


####################### Daten einlesen ####################################
df = pd.read_csv("/home/chris/PythonProjekte/SemProjekt-1920/tableFinal.txt", sep=";")
#df = pd.read_csv("tableFinal.csv", sep=";")
####################### Daten transformieren und neue Zeitspalten in Dataframe einfügen (Zeit) ########################
# Umrechnung der Start- & Endzeit in Minuten (für Simulationsuhr)
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

################################ Daten für Simulation erzeugen ##################################
# Gesamtanzahl an Fahrzeugen ermitteln
numberVeh = df["BlockID"].unique()
numberVeh = numberVeh.tolist()  # von Array in Liste formatieren
numberVeh = [elem for elem in numberVeh if elem >= 0]  # -1 entfernen
print("Die Gesamtanzahl von Fahrzeugen beträgt %d." % len(numberVeh))

# DepotID (jedem Fahrzeug die unique DepotID zuordnen)
DepotID = []
counter = 1
for i in range(1, len(numberVeh) + 1):
    for j in range(0, df.shape[0]):
        if df.BlockID[j] == i and counter == i:
            DepotID.append(df.DepotID[j])
            counter += 1
print("Es gibt %d verschiedene Depots." % (len(set(DepotID))))
print("Jedes Fahrzeug wurde einem Depot zugeordnet: %s." % (
        len(DepotID) == len(numberVeh)))

# StartTimes der einzelnen Fahrzeuge in jedem Teilumlauf (in Dictionary gespeichert)
DepotID_plusOne = [0] + DepotID  # DepotIDListe verlängern, damit Schleife mit i funktioniert
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
        {(
                 i - 1): startTimes_Block})  # i-1 damit Index bei 0 anfängt (wichtig für Schleife (nachträgliche Ãnderung!)

StartTime_dic = startTime_dic

numTU_proF = []
for i in range(0, len(numberVeh)):
    numTU_proF.append(len(StartTime_dic[i]) - 1)
print("Die Fahrzeuge fahren im Schnitt %d Teilumläufe am Tag."
      " Das Maximum ist %d und das Minimum %d." % (sum(numTU_proF) / len(numTU_proF), max(numTU_proF), min(numTU_proF)))

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

############################## Funktionen für Objekt Vehicle #############################

# Abfrage: Fahrtzeit über Simulationsdauer
def drive_outOfTime(time, clock):
    doOT = time + clock > 1440
    return doOT

########################### Funktionen für Störungen ##############################################
def delayCalculator(ausmaß, driveduration, delayonTop):
    delayperDisruption = 0
    coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
    if (coin == 1):
        delayperDisruption = int(driveduration * delayonTop)
    return delayperDisruption

def rushhour(time):
    if time >= RushhourStart1 and time <= RushhourEnde1: # Fahrtzeit liegt in RushHour
        return True
    elif time >= RushhourStart2 and time <= RushhourEnde2:
        return True
    else:
        return False

def weather(driveduration):
    delay = 0
    delayType = ""
    if varSturm.get() == 1: # Störungen durch Sturm
        ausmaß = ausmaßSturm
        delayactiveS = delayCalculator(ausmaß, driveduration, delaySturm)
        delay += delayactiveS
        if delayactiveS > 0:
            delayType += "|Sturm|"
    if varRegen.get() == 1:  # Störungen durch Regen
        ausmaß = ausmaßRegen
        delayactiveR = delayCalculator(ausmaß, driveduration, delayRegen)
        delay += delayactiveR
        if delayactiveR > 0:
            delayType += "|Regen|"
    return delay, delayType

def event(startHS, endHS):
    delay = 0
    delayType = ""
    if startHS in eventOrte or endHS in eventOrte:
        delay = delayEvent
        delayType = "|Event|"
    else:
        delay = 0
    return delay, delayType

#BaustellenListe = list(baustellenHS)  # Eingabe von Benutzer nutzen
def baustelle(startHS, endHS):
    delayonTop = 0
    delayType = ""
    if startHS in BaustellenListe or endHS in BaustellenListe:
        delayonTop = delayBaustelle
        delayType = "|Baustelle|"
    else:
        delayonTop = 0
    return delayonTop, delayType

def unfall(driveduration):
    delayType = ""
    delayactiveU = delayCalculator(ausmaßUnfall, driveduration, delayUnfall)
    delay = delayactiveU
    if delayactiveU > 0:
        delayType = "|Unfall|"
    return delay, delayType

def fahrzeugausfall():
    delay = 0
    delayType = ""
    coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaßAusfall, ausmaßAusfall])
    if (coin == 1):
        delay = 1440
        delayType = "|Fahrzeugausfall|"
    else:
        delay = 0
    return delay, delayType

"""
############# crazy Staufunktion ##############

####### Funktion: Stauausbruch zu bestimmten Zeiten #########################
def stauzeitGroup():
    staugroup = numpy.random.choice(numpy.arange(0, 3), p=[0.1, 0.25, 0.65])
    return staugroup

#Quelle von def choice und def spaced_choice: https://stackoverflow.com/questions/47950131/drawing-random-numbers-with-draws-in-some-pre-defined-interval-numpy-random-ch/47950676
def choice(low, high, delta, n_samples):  # delta = wieviel abstand zwischen den Werten
    draw = numpy.random.choice(high - low - (n_samples - 1) * delta, n_samples, replace=False)
    idx = numpy.argsort(draw)
    draw[idx] += numpy.arange(low, low + delta * n_samples, delta)
    return draw

def spaced_choice(i, n_samples):
    stauintervall = random.randint(0, 1)
    if i == 0:  # Schwachverkehrszeit
        if stauintervall == 0:
            draw = choice(1, 389, 1, n_samples)
        else:
            draw = choice(1201, 1440, 1, n_samples)
    elif i == 1:  # Normalverkehrzeit
        if stauintervall == 0:
            draw = choice(511, 869, 1, n_samples)
        else:
            draw = choice(1111, 1200, 1, n_samples)
    elif i == 2:  # Hauptverkehrszeit
        if stauintervall == 0:
            draw = choice(390, 510, 1, n_samples)
        else:
            draw = choice(870, 1110, 1, n_samples)
    return list(draw)

def flatList(list):
    flat_list = []
    for sublist in list:
        for item in sublist:
            flat_list.append(item)
    return flat_list

def stauEndzeitCalculator(list):
    stauEndzeiten = []
    for item in range(len(list)):
        stauDauer = random.randint(staudauerMin, staudauerMax)
        stauEndzeit = list[item] + stauDauer
        stauEndzeiten.append(stauEndzeit)
    return stauEndzeiten

def stauStartzeitCalculator(n):
    stauStartzeiten = []
    staugroups = [0, 0, 0]
    for i in range(n):
        staugroups[stauzeitGroup()] += 1
    for i in range(len(staugroups)):
        stauStartzeiten.append(spaced_choice(i, staugroups[i]))
    stauStartzeiten = flatList(stauStartzeiten)
    return stauStartzeiten


def stauOrtCalculator(n):
    stauOrte = []
    for i in range(n):  ##Anzahl an Haltestellen mit Stau
        x = numpy.random.choice(df.FromStopID)
        stauOrte.append(x)
    return stauOrte
'''
from collections import Counter
a = len(Counter(df.FromStopID).keys())
print(a)
b = Counter(df.FromStopID)
print(b)
'''
def stauGenerator(n):
    stauBeginn = stauStartzeitCalculator(n)
    stauEnde = stauEndzeitCalculator(stauBeginn)
    stauOrt = stauOrtCalculator(n)
    return stauBeginn, stauEnde, stauOrt

stauBeginn, stauEnde, stauOrt = stauGenerator(anzahlStaus)
"""

############################ Störgenerator##################################
# Ausmaß = Anteil an Fahrten, die von Störung betroffen sind
# delayonTop = Verspätung, die abhängig von Fahrtzeit on Top auf die Fahrtzeit raufkommt

# Werte müssen in die GUi aufgenommen werden (für Testzwecke hier entspannter zum Einstellen)
varWeather = 1
varEvent = 1 #Event-Funktion noch nicht funktionstüchtig
varBaustelle = 1
varUnfall = 1


def passengerDisruption(time, driveduration, startHS, endHS): # Funktion für die Verlängerung der Haltezeit
    delay = 0
    delayType = ""
    if rushhour(time):
        delay += delayRushhour
        delayType += "|Hauptverkehrszeit|"
    if varWeather == 1:
        delayWeather, delayTypeWeather = weather(driveduration)
        delay += delayWeather
        delayType += delayTypeWeather
    if varEvent == 1:
        delayEvent, delayTypeEvent = event(startHS, endHS)
        delay += delayEvent
        delayType += delayTypeEvent
    return delay, delayType


def trafficDisruption(startHS, endHS, driveduration, time):
    delay = 0
    delayType = ""
    if rushhour(time):
        delay += delayRushhour
        delayType += "|Hauptverkehrszeit|"
    if varWeather == 1:
        delayWeather, delayTypeWeather = weather(driveduration)
        delay += delayWeather
        delayType += delayTypeWeather
    if varEvent == 1:
        delayEvent, delayTypeEvent = event(startHS, endHS)
        delay += delayEvent
        delayType += delayTypeEvent
    if varBaustelle == 1:
        delayBau, delayTypeBau = baustelle(startHS, endHS)
        delay += delayBau
        delayType += delayTypeBau
    if varUnfall == 1:
        delayUnfall, delayTypeUnfall = unfall(driveduration)
        delay += delayUnfall
        delayType += delayTypeUnfall
    return delay, delayType
"""        
    if varRdmStaus.get() == 1:  # Verkehrsaufkommen
        if fromhs in stauOrt or tohs in stauOrt:
            i = 0
            while i < len(stauBeginn):
                if time >= stauBeginn[i] and time < stauEnde[i]:
                    ausmaß = 1
                    delayonTop = delayStau
                    coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
                    if (coin == 1):
                        delay += int(driveduration * delayonTop)
                        delayType += "|rdmStau|"
                    i += 1000
                else:
                    i += 1
    if varFahrzeugausfall.get() == 1:
        delayAusfall, delayTypeAusfall = fahrzeugausfall()
        delay += delayAusfall
        delayType += delayTypeAusfall
        """



def breaktime(vehID, teilumlaufnummer, fahrtnummer, delayTime):
    if varPufferzeit == 1:  
        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
            DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] = \
                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] - delayTime
            if DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] < 0:
                delayTime = abs(DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer])
                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] = 0
            else:
                delayTime = 0
    return delayTime


############################## Daten für CSV-Datei ###############################
# Header für CSV-Datei
print(
    "vehID Teilumlaufnummer Standort Dep/Arr Uhrzeit(Soll) Uhrzeit(Ist) Fahrtverspätung Gesamtverspätung Verspätungsursache",
    file=open("Eventqueue5.9.csv", "a"))


########################## Objekt Vehicle #########################################
def vehicle(env, vehID):  # Eigenschaften von jedem Fahrzeug
    while True:
        for teilumlaufnummer in range(0, len(StartTime_dic) - 1):  # Loop der durch die einzelnen Teilumläufe führt
            try:
                if StartTime_dic[vehID][teilumlaufnummer] - env.now >= 0:
                    delayTime = 0
                    yield env.timeout(
                        StartTime_dic[vehID][teilumlaufnummer] - env.now)
                else:
                    yield env.timeout(0)
                    delayTime = env.now - StartTime_dic[vehID][teilumlaufnummer]

                umlaufstatus = 1  # Wenn Startzeit erreicht, Fahrzeug im Umlauf (umlaufstatus = 1)

                while umlaufstatus == 1:  # while Fahrzeug im Umlauf
                    for fahrtnummer in range(0, len(FromHS_dic[vehID][teilumlaufnummer])):

                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            fahrtstatus = 2
                            delayPassenger = 0
                            delayTypePassenger = "-"
                        else:
                            fahrtstatus = 0  # 0 = Abfahrt / 1 = Ankunft / 2 = Pause

                            delayPassenger, delayTypePassenger = passengerDisruption(env.now,
                                                                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer],
                                                                FromHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                                                ToHS_dic[vehID][teilumlaufnummer][fahrtnummer])

                            delayTime_perStop = delayPassenger
                            delayType = delayTypePassenger

                        delayTime += delayPassenger
                        yield env.timeout(delayPassenger)

                        print(vehID + 1, teilumlaufnummer + 1, FromHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                              fahrtstatus, PartStartTime_dic[vehID][teilumlaufnummer][fahrtnummer], env.now,
                              delayTime_perStop, delayTime, delayType,
                              file=open("Eventqueue5.9.csv", "a"))

                        # Verspätung auf Fahrt ermitteln
                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            delayTime_perDrive = 0
                            delayType = "-"
                        else:
                            delayTraffic, delayTypeTraffic = trafficDisruption(
                                                                FromHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                                                ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                                                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer],
                                                                env.now)

                            delayTime_perDrive = delayTraffic
                            delayType = delayTypeTraffic

                        # Aufsummieren der Verspätungen im Teilumlauf
                        delayTime += delayTime_perDrive

                        # Abfrage, ob Fahrt auÃerhalb der Simulationszeit liegen würde
                        if drive_outOfTime(
                                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer], env.now):
                            yield env.timeout(1440)
                            break

                        # Abfrage, ob Pausenzeit & Verspätungszeit anpassen
                        delayTime = breaktime(vehID, teilumlaufnummer, fahrtnummer, delayTime)

                        # Timeout für Fahrtdauer zur nächsten Haltestelle
                        yield (
                            env.timeout(DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] + delayTime_perDrive))

                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            fahrtstatus = 2
                        else:
                            fahrtstatus = 1

                        # Abfrage ob Bus im Depot angekommen
                        if ToHS_dic[vehID][teilumlaufnummer][fahrtnummer] == DepotID[vehID]:
                            print(vehID + 1, teilumlaufnummer + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  fahrtstatus, PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  env.now, delayTime_perDrive, delayTime, delayType,
                                  file=open("Eventqueue5.9.csv", "a"))
                            umlaufstatus = 0
                        else:
                            print(vehID + 1, teilumlaufnummer + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  fahrtstatus, PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  env.now, delayTime_perDrive, delayTime, delayType,
                                  file=open("Eventqueue5.9.csv", "a"))

            except:
                if env.now >= 1440:  # to avoid RunTimeError: GeneratorExit
                    return False
                continue

            ########################## Simulationsumgebung ##############################


env = simpy.Environment()

# Initialisierung von Fahrzeugen
for i in range(0, len(numberVeh)):  # Anzahl von Fahrzeugen = len(numberVeh)
    env.process(vehicle(env, i))  # Inputdaten Eigenschaften Fahrzeugen
# Simulation starten und Laufzeit festlegen
env.run(until=1440)  # Ein Tag simulieren: in Minuten ausdrücken. 24h = 1440min