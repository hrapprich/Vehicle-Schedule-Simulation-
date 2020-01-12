# -*- coding: utf-8 -*-
"""

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

###################### Interface Störungen ####################################
# Ausmaß = Anteil an Fahrten, die von der Störung betroffen sind
# Delay = Verspätung (relativ zur Fahrtdauer der Fahrt), die zur Fahrtdauer hinzukommt

# Passagieraufkommen
ausmaßPA = 0.2 # 20% der Fahrten sind von Störung betroffen
delayPA = 0.2 # Fahrtdauer verlängert sich um 20%, wenn Störung auftritt
# Verkehrsaufkommen
anzahlStaus = 50 # pro Simulationstag
staudauerMin = 10 # wie lange hält der Stau mindestens an (in Minuten)
staudauerMax = 50 # wie lange hält der Stau maximal an (in Minuten)
delayStau = 0.5 # Fahrtdauer verlängert sich bei Stau um 50%
# Sturm
ausmaßSturm = 0.8 # 80 % der Fahrten sind von Störung betroffen
delaySturm = 0.6 # Fahrtdauer verlänget sich Sturm um 60%
# Regen
ausmaßRegen = 0.5 # 50 % der Fahrten sind von Störung betroffen
delayRegen = 0.4 # Fahrtdauer verlänget sich Sturm um 40%
# Fahrzeugausfall
ausmaßAusfall = 0.01 # 1% Wahrscheinlichkeit, dass Fahrzeug ausfällt (delay = 1440)
# Baustelle an bestimmten Haltestellen
baustellenHS = 29, 167, 83
delayBaustelle = 1 # Fahrtdauer bei Baustelle verdoppelt sich
# Unfall
ausmaßUnfall = 0.05 # 5% Wahrscheinlichkeit, dass Unfall während passiert (Fahrzeug nicht beteiligt)
delayUnfall = round(random.uniform(0.5,2),2) # Fahrtdauer bei Unfall variiert zwischen 0.5 & 2

######################## GUI Design #############################################
root = Tk()
root.geometry("700x700")
root.title('Simulationstool zur Überprüfung der Robustheit von Fahrzeugeinsatzplänen')
Überschrift = font.Font(family='Helvetica', size=11, weight='bold')
Text = font.Font(family="Helvetica", size=10)
Bestätigung = font.Font(family="Helvetica", size=11)

# 1 Eingabefelder anlegen und positionieren
Frame0 = Frame(root, bg="grey", padx=6, pady=6)
Frame0.grid(row=0, columnspan=8)
Frame1 = Frame(root, bg="grey", padx=6, pady=6)
Frame1.grid(row=5, columnspan=8)
Frame2 = Frame(root, bg="grey", padx=6, pady=6)
Frame2.grid(row=9, columnspan=8)
Frame3 = Frame(root, bg="grey", padx=6, pady=6)
Frame3.grid(row=12, columnspan=8)
Frame4 = Frame(root, bg="grey", padx=6, pady=6)
Frame4.grid(row=15, columnspan=8)
# Frame5 = Frame(root, bg = "grey", padx=6, pady=6)
# Frame5.grid(row=1, columnspan = 8)


# label1 = Label(Frame1, text="Wochentag").grid(row=0,columnspan=5)
label0 = Label(Frame0, text="Wochentag", width=50, height=1, bg="grey", font=Überschrift).grid(row=0)
label1 = Label(Frame1, text="Globale Einstellungen", width=50, height=1, bg="grey", font=Überschrift).grid(row=5)
label2 = Label(Frame2, text="Verkehrslage", width=50, height=1, bg="grey", font=Überschrift).grid(row=9)
label3 = Label(Frame3, text="Wetter", width=50, height=1, bg="grey", font=Überschrift).grid(row=12)
label4 = Label(Frame4, text="Specials", width=50, height=1, bg="grey", font=Überschrift).grid(row=15)

button = Button(text="Bestätigen", bg="green", width=20, height=2, font=Bestätigung, command=root.destroy)
button.grid(row=19, column=0, columnspan=5, sticky=S + W)

# 2 Checkbutton anlegen
WochentagFerien = IntVar()
Checkbutton1 = Checkbutton(root, text="Wochentag - Ferien", font=Text, variable=WochentagFerien)
Checkbutton1.grid(row=1, column=2, columnspan=5, sticky=W)

WochentagNoFerien = IntVar()
Checkbutton2 = Checkbutton(root, text="Wochentag - Keine Ferien", font=Text, variable=WochentagNoFerien)
Checkbutton2.grid(row=2, column=2, columnspan=5, sticky=W)

Samstag = IntVar()
Checkbutton3 = Checkbutton(root, text="Samstag", font=Text, variable=Samstag)
Checkbutton3.grid(row=3, column=2, columnspan=5, sticky=W)

Sonntag = IntVar()
Checkbutton4 = Checkbutton(root, text="Sonntag", font=Text, variable=Sonntag)
Checkbutton4.grid(row=4, column=2, columnspan=5, sticky=W)

varPassagieraufkommen = IntVar()
Checkbutton1 = Checkbutton(root, text="Erhöhtes Passagieraufkommen an einigen Haltestellen", font=Text,
                           variable=varPassagieraufkommen)
Checkbutton1.grid(row=6, column=2, columnspan=7, sticky=W)

varVerkehrsaufkommen = IntVar()
Checkbutton2 = Checkbutton(root, text="Erhöhtes Verkehrsaufkommen an einigen Haltestellen", font=Text,
                           variable=varVerkehrsaufkommen)
Checkbutton2.grid(row=7, column=2, columnspan=7, sticky=W)

varPufferzeit = IntVar()
Checkbutton3 = Checkbutton(root, text="Pufferzeiten für Abbau von Verspätungen nutzen", font=Text,
                           variable=varPufferzeit)
Checkbutton3.grid(row=8, column=2, columnspan=7, sticky=W)

varUnfall = IntVar()
Checkbutton4 = Checkbutton(root, text="Unfall auf Strecke", font=Text, variable=varUnfall)
Checkbutton4.grid(row=10, column=2, columnspan=5, sticky=W)

label5 = Label(root, text="Baustelle an folgender Haltestelle:", font=Text).grid(row=11, column=2, columnspan=7,
                                                                                 sticky=W)
varBaustelle = IntVar()
e1 = Entry(root).grid(row=11, column=7, sticky=W)
# Checkbutton5 = Checkbutton(root, text = "Baustelle an bestimmter Haltestelle (hier: HS 29)", font = Text, variable = varBaustelle)
# Checkbutton5.grid(row = 11, column = 4, columnspan=1, sticky=W)

varSturm = IntVar()
Checkbutton6 = Checkbutton(root, text="An diesem Tag gibt es Sturm.", font=Text, variable=varSturm)
Checkbutton6.grid(row=13, column=2, columnspan=5, sticky=W)

varRegen = IntVar()
Checkbutton7 = Checkbutton(root, text="An diesem Tag regnet es.", font=Text, variable=varRegen)
Checkbutton7.grid(row=14, column=2, columnspan=5, sticky=W)

varFahrzeugausfall = IntVar()
Checkbutton8 = Checkbutton(root, text="Fahrzeug fällt mit 1% Wahrscheinlichkeit aus.", font=Text,
                           variable=varFahrzeugausfall)
Checkbutton8.grid(row=16, column=2, columnspan=7, sticky=W)

label6 = Label(root, text="Prozentuales Ausmaß an Verspätung:", font=Text).grid(row=17, column=2, columnspan=7,
                                                                                sticky=W)
Stau = IntVar()
Scalebutton = Scale(root, from_=0, to=100, length=250, tickinterval=10, orient=HORIZONTAL, troughcolor="black",
                    width=30, variable=Stau)
Scalebutton.grid(row=18, column=2, columnspan=5, sticky=W)

root.mainloop()

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

"""
###export_csv = tableFinal.to_csv(r'TESTtableFinal.csv', index=None, header=True)


####################### Daten einlesen ####################################
#df = pd.read_csv("/home/chris/PythonProjekte/SemProjekt-1920/tableFinal.txt", sep=";")
df = pd.read_csv("tableFinal.csv", sep=";")
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

####### Funktion: Stauausbruch zu bestimmten Zeiten #########################
def stauzeitGroup():
    staugroup = numpy.random.choice(numpy.arange(0, 3), p=[0.1, 0.25, 0.65])
    return staugroup

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
#print("Staubeginn: ", stauBeginn)
#print("StauEnde: ", stauEnde)
#print("Stauort: ", stauOrt)

############################## Funktionen für Objekt Vehicle #############################

# Abfrage: Fahrtzeit über Simulationsdauer
def drive_outOfTime(time, clock):
    doOT = time + clock > 1440
    return doOT


############################ Störgenerator##################################
# Ausmaß = Anteil an Fahrten, die von Störung betroffen sind
# delayonTop = Verspätung, die abhängig von Fahrtzeit on Top auf die Fahrtzeit raufkommt
def globalDisruption(driveduration, time):
    delay = 0
    delayType = ""
    if varPassagieraufkommen.get() == 1:  # Passagieraufkommen
        ausmaß = ausmaßPA
        delayonTop = delayPA
        coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
        if (coin == 1):
            delay += int(driveduration * delayonTop)
            delayType += "PA"
    if varSturm.get() == 1:  # Sturm
        ausmaß = ausmaßSturm
        delayonTop = delaySturm
        coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
        if (coin == 1):
            delay += int(driveduration * delayonTop)
            delayType += ", Sturm"
    if varRegen.get() == 1:  # Regen
        ausmaß = ausmaßRegen
        delayonTop = delayRegen
        coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
        if (coin == 1):
            delay += int(driveduration * delayonTop)
            delayType += ", Regen"
    if varFahrzeugausfall.get() == 1:
        ausmaß = ausmaßAusfall
        coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
        if (coin == 1):
            delay = 1440
            delayType += ", Fahrzeugausfall"
    return delay, delayType  # Type der Störung bei Ausgabe angeben (durch Input Checkbox bestimmt)(Funktion immer dieselbe)


BaustelleanbestimmterHS = list(baustellenHS)  # Eingabe von Benutzer nutzen
def selectionDisruption(fromhs, tohs, driveduration, time):
    delay = 0
    delayType = ""
    if varVerkehrsaufkommen.get() == 1:  # Verkehrsaufkommen
        if fromhs in stauOrt or tohs in stauOrt:
            i = 0
            while i < len(stauBeginn):
                if time >= stauBeginn[i] and time < stauEnde[i]:
                    ausmaß = 1
                    delayonTop = delayStau
                    coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
                    if (coin == 1):
                        delay += int(driveduration * delayonTop)
                        delayType += ", Stau"
                    i += 1000
                else:
                    i += 1
    if varBaustelle.get() == 1:
        if fromhs in BaustelleanbestimmterHS or tohs in BaustelleanbestimmterHS:
            ausmaß = 1
            delayonTop = delayBaustelle
            coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
            if (coin == 1):
                delay += int(driveduration * delayonTop)
                delayType += ", Baustelle"
    if varUnfall.get() == 1:
        ausmaß = ausmaßUnfall
        delayonTop = delayUnfall
        coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
        if (coin == 1):
            delay += int(driveduration * delayonTop)
            delayType += ", Unfall"
    return delay, delayType  # Type der Störung bei Ausgabe angeben (durch Input Checkbox bestimmt)(Funktion immer dieselbe)


def breaktime(vehID, teilumlaufnummer, fahrtnummer, delayTime):
    if varPufferzeit.get() == 1:
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
print("Staubeginn: ", stauBeginn)
print("Stauende: ", stauEnde)
print("Stauorte: ", stauOrt)
print("Baustellen an HS: ", BaustelleanbestimmterHS)
# Header für CSV-Datei
print(
    "vehID Teilumlaufnummer Standort Dep/Arr Uhrzeit(Soll) Uhrzeit(Ist) Fahrtverspätung Gesamtverspätung Verspätungsursache",
    file=open("Eventqueue5.6.csv", "a"))


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
                        else:
                            fahrtstatus = 0  # 0 = Abfahrt / 1 = Ankunft / 2 = Pause

                        delayTime_perDrive = 0  # für PrintAusgabe hier definiert
                        print(vehID + 1, teilumlaufnummer + 1, FromHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                              fahrtstatus, PartStartTime_dic[vehID][teilumlaufnummer][fahrtnummer], env.now,
                              "-", delayTime, "-",
                              file=open("Eventqueue5.6.csv", "a"))

                        # Verspätung auf Fahrt ermitteln
                        delayType = ""
                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            delayTime_perDrive = 0
                            delayType = "-"
                        else:
                            delayGlobal, delayTypeGlobal = globalDisruption(
                                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer],
                                env.now)
                            delaySelection, delayTypeSelection = selectionDisruption(
                                FromHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer],
                                env.now)

                            delayTime_perDrive = delayGlobal + delaySelection
                            delayType = delayTypeGlobal + " " + delayTypeSelection

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
                                  file=open("Eventqueue5.6.csv", "a"))
                            umlaufstatus = 0
                        else:
                            print(vehID + 1, teilumlaufnummer + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  fahrtstatus, PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  env.now, delayTime_perDrive, delayTime, delayType,
                                  file=open("Eventqueue5.6.csv", "a"))

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
