# -*- coding: utf-8 -*-
"""
Damit das Tool genutzt werden kann:
Zunächst muss die Library simpy installiert werden, welches die eigentliche Simulation ausführt. 
Dafür im cmd den Befehl "pip install simpy" ausführen.
Ebenso muss tkinter installiert werden, mittels des Befehls "pip install ttk themes". Das ist nötig, um die GUI
zu nutzen.
Damit die Daten eingelesen werden können:
Den Ordner "opti", welcher alle Daten inkludiert, am selben Ort, an dem die Pythondatei abgespeichert ist.
Der opti Ordner muss die Unterordner "Mo_Ferien", "Mo_Schule", "Samstag" und "Sonntag" besitzen.
In den jeweiligen Ordnern müssen eine timetable.txt, timetable-blocks.txt und eine timetable-duties.txt Datei hinterlegt sein.
"""
###############################################################################
########################### Interface Störungen ###############################
###############################################################################
"""
In diesem Bereich können die Störungsgeneratoren manuell ein- bzw. ausgeschaltet werden.
Auch wenn in der GUI Input eingegeben wird, die Generatoren hier allerdings manuell ausgeschaltet sind,
werden keine Störungen erzeugt. 
Ebenso bietet der Bereich die Möglichkeit die Ausmaße festzulegen, die die Stärke der Störungen
definieren.
"""

# **************** Wetter *******************

varWeather = 1 # 0 für aus; 1 für an: Hierdurch werden sowohl Regen als auch Sturm gesteuert.

# Wahrscheinlichkeit, dass Sturm Fahrt- & Haltezeit beeinflusst; In diesem Fall mindestens 60% und maximal 100%
wktSturm_Min, wktSturm_Max = 0.6, 1 

# Diese Variablen legen die Stärke der Störung "Sturm" fest. 
#Fahrt- & Haltedauer werden hier mindestens zu 40% und maximal zu 80% erhöht.
delaySturm_Min, delaySturm_Max = 0.4, 0.8 # 

wktRegen_Min, wktRegen_Max = 0.1, 0.3  # 10%-30% Wahrscheinlichkeit, dass Regen Fahrt- & Haltezeit beeinlusst
delayRegen_Min, delayRegen_Max = 0.1, 0.2 # Fahrt- & Haltedauer verlängert sich um 10-20%

# **************** Rushhour Ferien*****************

varRushhour = 1 # 0 für aus; 1 für an: Hierdurch wird die Störung "Berufsverkehr" gesteuert.
# Im Folgenden werden die Start- & Endzeiten der Rushhour festgelegt.
# Die Uhrzeiten werden in ganzen Minuten ausgedrückt. 1:00 Uhr entspricht also 60, 2:00 entspricht 120 usw.

RushhourStart1, RushhourEnde1  = 390, 510 # Entspricht 6:30 Uhr - 8:30 Uhr
RushhourStart2, RushhourEnde2 = 870, 1110 # Entspricht 14:30 Uhr - 18:30 Uhr

# Wahrscheinlichkeit, dass Berufsverkehr Fahrt- & Haltezeit beeinflusst; In diesem Fall mindestens 10% und maximal 30%
delayRushhour_Min, delayRushhour_Max = 0.05, 0.15

# Diese Variablen legen die absolute Erhöhung der Zeiten durch die Störung "Berufsverkehr" fest. 
# Fahrt- & Haltedauer werden hier mindestens um 2 Minuten und maximal um 2 Minuten erhöht.
delayRushhour_Halt_Min, delayRushhour_Halt_Max = 0, 1 
'''
# ***************** Rushhour keine Ferien *******************
varRushhour = 1 # 0 für aus; 1 für an
RushhourStart1, RushhourEnde1  = 390, 510 # Rushhour zwischen 6:30 und 8:30
RushhourStart2, RushhourEnde2 = 870, 1110 # Rushhour zwischen 14:30 und 18:30
delayRushhour_Min, delayRushhour_Max = 0.1, 0.3  # Fahrtdauer verlängert sich um 10-30%
delayRushhour_Halt_Min, delayRushhour_Halt_Max = 0, 2 # 0-2 Minuten mehr Haltezeit
'''
# **************** Event ********************

varEvent = 1 # 0 für aus; 1 für an: Hierdurch wird die Störung "Veranstaltung" gesteuert.

# Diese Variablen legen die Stärke der Störung "Veranstaltung" für Fahrtzeiten fest. 
# Fahrtzeiten werden hier mindestens zu 20% und maximal zu 80% erhöht.
delayEvent_Min, delayEvent_Max = 0.2, 0.8

# Diese Variablen legen die Stärke der Störung "Veranstaltung" für Haltezeiten fest. 
# Haltezeiten werden hier mindestens um 1 Minute und maximal um 4 Minuten erhöht.
delayEvent_Halt_Min, delayEvent_Halt_Max = 1, 4

# **************** Baustelle ****************

varBaustelle = 1 # 0 für aus; 1 für an: Hierdurch wird die Störung "Baustelle" gesteuert.

# Fahrtzeiten werden hier mindestens um 4 Minuten und maximal um 8 Minuten erhöht.
delayBaustelle_Min, delayBaustelle_Max = 4, 8 

# **************** Sperrung *****************

varSperrung = 1 # 0 für aus; 1 für an: Hierdurch wird die Störung "Sperrung" gesteuert.
# Diese Variablen legen die Stärke der Störung "Sperrung" für Fahrtzeiten fest. 
#Fahrtzeiten werden hier mindestens um 10% und maximal um 30% erhöht.
delaySperrung_Min, delaySperrung_Max = 0.1, 0.3

# **************** Unfall *******************
varUnfall = 1 # 0 für aus; 1 für an: Hierdurch wird die Störung "Unfall" gesteuert.

anzahlUnfaelle = 10  # Hierdurch wird festgelegt, wie viele Unfälle zufällig generiert werden. (Funktion siehe weiter unten)
staudauerMin = 30  # Hierdurch wird festgelegt, wie lange ein Unfall mindestens auftritt.
staudauerMax = 120  # Hierdurch wird festgelegt, wie lang ein Unfall maximal auftritt.

# Diese Variablen legen die Stärke der Störung "Unfall" für Fahrtzeiten fest. 
# Fahrtzeiten werden hier mindestens um 30% und maximal um 60% erhöht.
delayStau_Min, delayStau_Max = 0.3, 0.6

# **************** Leerfahrten **************

varLeerfahrt = 1 #0, wenn Leerfahrten nicht zum Pufferabbau genutzt werden sollen
avgPaceIncrease = 0.2 # um wie viel % fährt ein Fahrzeug schneller bei Leerfahrten

'''
# ****************2 Unfälle am Tag **************************
varUnfall = 1 # 0 für aus; 1 für an
anzahlUnfaelle = 2  # 2 Unfälle pro Simulationstag
staudauerMin = 15  # wie lange hält der Stau mindestens an (in Minuten)
staudauerMax = 60  # wie lange hält der Stau maximal an (in Minuten)
delayStau_Min, delayStau_Max = 0.2, 0.6 # Fahrtdauer verlängert sich um 20-60%
'''

###############################################################################
########################### Import Packages ###################################
###############################################################################
import simpy
import pandas as pd
import numpy
import random
from random import randint
from tkinter import *
from tkinter import font
import tkinter.ttk as ttk
import sys, datetime as dt
from io import StringIO

###############################################################################
####################### Graphical User Interface ##############################
###############################################################################

root = Tk() # Damit das GUI Fenster erstellt werden kann
s = ttk.Style() #Damit der Style im Fenster geändert werden kann.
s.theme_use('clam')# Wählbare Themes:'winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'

#Diverse nötige Einstellungen, wie die Größe des Fensters und Schriftarten
root.resizable(width=False, height=False)
root.geometry('+0+0')
root.title('Simulationstool zur Überprüfung der Robustheit von Fahrzeugeinsatzplänen')
s.configure('TButton', background='green', padding=(50, 10), font=('Verdana', 10, 'bold'))
Überschrift = font.Font(family='Verdana', size=11, weight='bold')
Überschrift2 = font.Font(family='Verdana', size=10, weight='bold')
Text = font.Font(family="Verdana", size=9)
Text = font.Font(family="Verdana", size=9)
Bestätigung = font.Font(family="Verdana", size=11, weight="bold")

# 1. Design der Teilüberschriften
Frame0 = Frame(root, bg="grey", padx=6, pady=6)
Frame0.grid(row=0, columnspan=8)
Frame1 = Frame(root, bg="grey", padx=6, pady=6)
Frame1.grid(row=7, columnspan=8)
Frame2 = Frame(root, bg="grey", padx=6, pady=6)
Frame2.grid(row=14, columnspan=8)

# 2. Labels der einzelnen Teilüberschriften (Anordnung über row & column)
Label(Frame0, text="Einstellungen", width=50, height=1, bg="grey", font=Überschrift).grid(row=0)
Label(Frame1, text="Globale Störungsmuster", width=50, height=1, bg="grey", font=Überschrift).grid(row=7)
Label(Frame2, text="Selektive Störungsmuster", width=50, height=1, bg="grey", font=Überschrift).grid(row=13)

# 3. Labels der einzelnen Unterüberschriften und die Schriftzüge
Label(text="Wetter", width=20, height=1, bg="darkgrey", font=Überschrift2).grid(row=8, column=2)
Label(text="Unfall", width=20, height=1, bg="darkgrey", font=Überschrift2).grid(row=8, column=5)
Label(text="Veranstaltung", width=20, height=1, bg="darkgrey", font=Überschrift2).grid(row=15, column=2)
Label(text="Baustelle", width=20, height=1, bg="darkgrey", font=Überschrift2).grid(row=19, column=2)
Label(text="Sonstige Sperrungen", width=20, height=1, bg="darkgrey", font=Überschrift2).grid(row=21, column=2)
Label(root, text="  Folgender Wochentag soll", font=Text).grid(row=1, column=2, columnspan=3, sticky=W)
Label(root, text="  simuliert werden:", font=Text).grid(row=2, column=2, columnspan=3, sticky=W)
Label(root, text="  Sollten Wartezeiten zum Abbau", font=Text).grid(row=3, column=2, columnspan=3, sticky=W)
Label(root, text="  von Verspätungen genutzt werden?", font=Text).grid(row=4, column=2, columnspan=3, sticky=W)
Label(root, text="  Sollten Pausenzeiten zum Abbau", font=Text).grid(row=5, column=2, columnspan=3, sticky=W)
Label(root, text="  von Verspätungen genutzt werden?", font=Text).grid(row=6, column=2, columnspan=3, sticky=W)
Label(root, text="  Event nahe der Haltestelle(n):", font=Text).grid(row=16, column=2, columnspan=3, sticky=W)
Label(root, text="  In welcher Zeitspanne findet", font=Text).grid(row=17, column=2, columnspan=1, sticky=W)
Label(root, text="  das Event statt?", font=Text).grid(row=18, column=2, columnspan=1, sticky=W)
Label(root, text="  Baustelle nahe der Haltestelle(n):", font=Text).grid(row=20, column=2, columnspan=3, sticky=W)
Label(root, text="  Straßensperrungen nahe der:", font=Text).grid(row=22, column=2, columnspan=3, sticky=W)
Label(root, text="  Haltestelle(n):", font=Text).grid(row=23, column=2, columnspan=3, sticky=W)

# 4. Button zur Bestätigung, die das Fenster auch wieder schließt. Notwendig, da sonst restlicher Code nicht laufen würde.
button = ttk.Button(text="Bestätigen", style='TButton', command=root.destroy)
button.grid(row=26, column=0, columnspan=5, sticky=S + W)

# 5. Dropdownboxen zum Auswählen der jeweiligen Fahrpläne/Tage,ob Pufferzeit & Pausenzeiten genutzt werden können.
chosenDay = StringVar()
day = ttk.Combobox(root, textvariable=chosenDay)
day['values'] = ["Arbeitstag - Keine Ferien", "Arbeitstag - Ferien", "Samstag", "Sonntag"]
day.grid(row=2, column=5, sticky=W)
day.current(0)

varPufferzeit = StringVar()
pufferzeit = ttk.Combobox(root, textvariable=varPufferzeit, width=8)
pufferzeit['values'] = ["Ja", "Nein"]
pufferzeit.grid(row=4, column=5, sticky=W)
pufferzeit.current(0)

varPausenzeit = StringVar()
pausenzeit = ttk.Combobox(root, textvariable=varPausenzeit, width=8)
pausenzeit['values'] = ["Ja", "Nein"]
pausenzeit.grid(row=6, column=5, sticky=W)
pausenzeit.current(1)

# 6. Hier werden die einzelnen Checkboxen definiert.
varSturm = IntVar()
Checkbutton9 = Checkbutton(root, text="Sturm", font=Text, variable=varSturm)
Checkbutton9.grid(row=9, column=2, columnspan=3, sticky=W)

varRegen = IntVar()
Checkbutton10 = Checkbutton(root, text="Regen", font=Text, variable=varRegen)
Checkbutton10.grid(row=10, column=2, columnspan=3, sticky=W)

varUnfallGUI = IntVar()
Checkbutton11 = Checkbutton(root, text="Unfälle während des Umlaufs", font=Text, variable=varUnfallGUI)
Checkbutton11.grid(row=9, column=5, columnspan=3, sticky=W)

#7. Hier werden die einzelnen Freitextfelder definiert.
varVeranstaltung = StringVar()
Entry(root, textvariable=varVeranstaltung).grid(row=16, column=5, sticky=W)

varVeranstaltungZeit = StringVar(value='hh:mm - hh:mm')
Entry(root, textvariable=varVeranstaltungZeit).grid(row=18, column=5, sticky=W)

varBaustellen = StringVar()
Entry(root, textvariable=varBaustellen).grid(row=20, column=5, sticky=W)

sperrungen = StringVar()
Entry(root, textvariable=sperrungen).grid(row=23, column=5, sticky=W)

root.mainloop() #Hierdurch wird der GUI Befehl abgeschlossen.

# 8. Die Daten aus den Freitextfeldern werden hierdurch aufbereitet und 
#    von String Variablen in nutzbare Arrays umgewandelt. (Durch split Befehl)
if varVeranstaltung.get() != (""):
    eventOrte = varVeranstaltung.get().split(',')
    for i in range(len(eventOrte)):
        eventOrte[i] = int(eventOrte[i])
else:
    eventOrte = []

if varBaustellen.get() != (""):
    BaustellenListe = varBaustellen.get().split(',')
    for i in range(len(BaustellenListe)):
        BaustellenListe[i] = int(BaustellenListe[i])
else:
    BaustellenListe = []

if sperrungen.get() != (""):
    SperrungListe = sperrungen.get().split(',')
    for i in range(len(SperrungListe)):
        SperrungListe[i] = int(SperrungListe[i])
else:
    SperrungListe = []

if varPufferzeit.get() == "Ja":
    varPufferzeit = 1
else:
    varPufferzeit = 0

if varVeranstaltungZeit.get() == ("") or varVeranstaltungZeit.get() == ("hh:mm - hh:mm"):
    VeranstaltungZeit = []
else:
    VeranstaltungZeit = varVeranstaltungZeit.get().split('-')
    eventStarttime = VeranstaltungZeit[0].split(':')
    eventEndtime = VeranstaltungZeit[1].split(':')
    eventStarttime = int(eventStarttime[0]) * 60 + int(eventStarttime[1])
    eventEndtime = int(eventEndtime[0]) * 60 + int(eventEndtime[1])

###############################################################################
########################## Einleseroutine #####################################
###############################################################################

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
            if curr_row == '':      break  ### Empty (last) row found
            if curr_row[0] == '*':  continue  ### Comment found
            if curr_row[0] == '$':  ### New table found
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

# Diese Funktion liest je nachdem welchen Tag der Anwender in der GUI ausgewählt hat,
# die Daten des passenden Tages aus.
def dayChoice(chosenDay):
    if chosenDay == "Arbeitstag - Keine Ferien":
        data = load_table_data('opti/Mo_Schule/timetable.txt')
        blockdata = load_table_data('opti/Mo_Schule/timetable-blocks.txt')
        dutydata = load_table_data('opti/Mo_Schule/timetable-duties.txt')
        return (data, dutydata, blockdata)
    elif chosenDay == "Arbeitstag - Ferien":
        data = load_table_data('opti/Mo_Ferien/timetable.txt')
        blockdata = load_table_data('opti/Mo_Ferien/timetable-blocks.txt')
        dutydata = load_table_data('opti/Mo_Ferien/timetable-duties.txt')
        return (data, dutydata, blockdata)
    elif chosenDay == "Samstag":
        data = load_table_data('opti/Samstag/timetable.txt')
        blockdata = load_table_data('opti/Samstag/timetable-blocks.txt')
        dutydata = load_table_data('opti/Samstag/timetable-duties.txt')
        return (data, dutydata, blockdata)
    elif chosenDay == "Sonntag":
        data = load_table_data('opti/Sonntag/timetable.txt')
        blockdata = load_table_data('opti/Sonntag/timetable-blocks.txt')
        dutydata = load_table_data('opti/Sonntag/timetable-duties.txt')
        return (data, dutydata, blockdata)

data, dutydata, blockdata = dayChoice(chosenDay.get()) # Führt die obere Funktion aus.


# Relevante Dataframes werden aus den ausgewählten Datensätzen extrahiert.
servicefahrten = data["$SERVICEJOURNEY"]
dutyelements = dutydata["$DUTYELEMENT"]
blocks = blockdata["$BLOCK"]
dutytype = dutydata["$DUTY"]
# Das Dataframe "tableFinal" bietet die Grundlage für die später genutzte Datenbasis.
# Schritt für Schritt werden die notwendigen Daten aus den verschiedenen Datensätzen zusammengeführt.
tableFinal = dutyelements
allLines = servicefahrten
tableFinal = tableFinal.drop(
    ['ServiceJourneyCode', 'TransferType', 'GroupTransferIndex', 'DeadRunTransferBlockID', 'DeadRunTransferDutyID'],
    axis=1)
LineID = []
Distance = []
count_rows_duty = dutyelements.shape[0]
count_rows_dutytype = dutytype.shape[0]
count_rows_service = servicefahrten.shape[0]
count_blocks = blocks.shape[0]

# Wenn die ServiceJourneyID aus dem Dataframe tableFinal mit der ID aus den Servicefahrten übereinstimmt
# dann wird die LineID und Distance hinzugefügt. Andernfalls kann beides nicht zugeordnet werden und 
# muss auf 0 gesetzt werden. (Kann nicht für das Tool verwendet werden.)
for x in range(count_rows_duty):
    for y in range(count_rows_service):
        if tableFinal.iat[x, 2] == allLines.iat[y, 0]:
            LineID.append(allLines.iat[y, 1])
            Distance.append(allLines.iat[y, 17])
    if tableFinal.iat[x, 2] == -1:
        LineID.append(0)
        Distance.append(0)

VehTypeID = []
DepotID = []
for x in range(count_rows_duty):
    if tableFinal.iat[x, 1] == -1:
        VehTypeID.append(tableFinal.iat[(x + 1), 1])
        DepotID.append(tableFinal.iat[x, 4])
    else:
        for y in range(count_blocks):
            if tableFinal.iat[x, 1] == blocks.iat[y, 0]:
                VehTypeID.append(blocks.iat[y, 1])
                DepotID.append(blocks.iat[y, 2])
                
# für diese Simulation nicht notwendig, da Dienstplandaten nicht erhalten
df_dutytype = []
for x in range(count_rows_duty):
    for y in range(count_rows_dutytype):
        if tableFinal.iat[x, 0] == dutytype.iat[y, 0]:
            df_dutytype.append(dutytype.iat[y, 1])
tableFinal["DutyType"] = df_dutytype
tableFinal["DepotID"] = DepotID
tableFinal["VehTypeID"] = VehTypeID
tableFinal["LineID"] = LineID
tableFinal["Distance"] = Distance
df = tableFinal

# export_csv = tableFinal.to_csv(r'tableFinal.csv', index=None, header=True)

###############################################################################
######################## Data Preparation #####################################
###############################################################################

# Im Datensatz "Arbeitstag - Keine Ferien" gab es eine Dateninkonsistenz.
# Das Fahrzeug ist fälschlicherweise nach einem Teilumlauf nicht zurück ins Depot gefahren.
# Damit die Simulation den Teilumlauf abschließen kann, wird hier manuell die Haltestelle
# durch das Depot ersetzt.
pd.set_option('mode.chained_assignment', None)
if (chosenDay.get() == "Arbeitstag - Keine Ferien"):
    df.ToStopID[111] = 323    
    
# **************** Daten einlesen ***********

# Falls die Einleseroutine nicht nicht jedes mal ausgeführt werden soll, einfach 
# das Dataframe tableFinal als csv speichern und in der nächsten Zeile wieder einlesen.
# Spart mehrere Minuten Rechenzeit.
#df = pd.read_csv("tableFinal.csv", sep=";") 

# **************** Daten transformieren *****
    
# Damit die Simulationsuhr mit den Uhrzeiten rechnen kann, werden die Zeiten in Minuten
# umgerechnet.

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


# Gesamtanzahl an Fahrzeugen ermitteln
numberVeh = df["BlockID"].unique()
numberVeh = numberVeh.tolist()  # von Array in Liste formatieren
numberVeh = [elem for elem in numberVeh if elem >= 0]  # -1 entfernen
print("Fahrzeuge: %d " % len(numberVeh), file=open("Output.txt", "a"))


# Hierdurch wird eine Liste der DepotID eines jeden Fahrzeugs erstellt.
DepotID = []
counter = 1
for i in range(1, len(numberVeh) + 1):
    for j in range(0, df.shape[0]):
        if df.BlockID[j] == i and counter == i:
            DepotID.append(df.DepotID[j])
            counter += 1
print("Depots: %d " % (len(set(DepotID))), file=open("Output.txt", "a"))
print("Jedes Fahrzeug wurde einem Depot zugeordnet: %s." % (
        len(DepotID) == len(numberVeh)), file=open("Output.txt", "a"))

# Startzeiten der einzelnen Teilumläufe der Fahrzeuge werden in Dictionaries gespeichert.
# Dies ist sehr wichtig für die spätere Simulation.
DepotID_plusOne = [0] + DepotID  # DepotIDListe verlängern, damit Schleife mit i funktioniert
StartTime_dic = {}
for i in range(1, len(numberVeh) + 1):
    startTimes_Block = []
    for j in range(len(df)):
        if df.BlockID[j] == i:
            if df.FromStopID[j] == DepotID_plusOne[i]:
                startTimes_Block.append(df.StartTime[j])
    startTimes_Block = startTimes_Block + [
        1440]  # Damit die Simulation einwandfrei funktioniert, muss jedem Fahrzeug eine Endzeit von 1440(entspricht 24 Uhr) hinzugefügt werden.
    StartTime_dic.update(
        {(
                 i - 1): startTimes_Block})  # i-1 damit Index bei 0 anfängt (wichtig für Schleife)

# Lediglich relevant für den Output in der Konsole.
numTU_proF = []
for i in range(0, len(numberVeh)):
    numTU_proF.append(len(StartTime_dic[i]) - 1)
print("Die Fahrzeuge fahren im Schnitt %d Teilumläufe am Tag."
      " Das Maximum ist %d und das Minimum %d." % (round(sum(numTU_proF) / len(numTU_proF)), max(numTU_proF), min(numTU_proF)), file=open("Output.txt", "a"))

# Listen aus Listen bestehend aus Haltestellen (from/to)
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


# Im Folgenden werden in einer großen Schleife alle relevanten Dictionaries für die Simulation erstellt.
# Die Daten zu jeder einzelnen Fahrt sind in jedem Dictionary an der selben Stelle abgespeichert.
# Hierdurch können Daten in der Simulation simpel abgerufen werden. 

DriveDuration_dic = {}
FromHS_dic = {}
ToHS_dic = {}
PartStartTime_dic = {}
PartEndTime_dic = {}
ElementID_dic = {}
Distance_dic = {}

for i in range(1, len(numberVeh) + 1):
    # Für jedes Attribut wird eine leere Liste für alle Umläufe des Fahrzeugs und 
    # eine leere Liste für die Teilumläufe des Fahrzeugs erstellt.
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

    Distanz = []
    TeilumlaufDistanz = []

    for j in range(0, count_row):
        # es wird durch das gesamte Dataframe durchiteriert. Wenn BlockID (Fahrzeugnummer)
        # gleich i ist, werden die einzelnen Informationen in eine Variable gespeichert.
        if df.BlockID[j] == i:

            difTime = df.EndTime[j] - df.StartTime[j]
            fromhs = df.FromStopID[j]
            tohs = df.ToStopID[j]
            stTime = df.StartTime[j]
            eTime = df.EndTime[j]
            elementID = df.ElementType[j]
            distance = df.Distance[j]
            # wenn die Haltestelle, an die das Fahrzeug fährt, gleich dem Depot des Fahrzeugs ist,
            # dann werden die Variablen den oben erstellten Listen für die Teilumläufe hinzugefügt.
            # Diese Listen wiederum werden den Listen der gesamten Umläufe hinzugefügt.
            # Wenn das nicht der Fall ist (siehe else Bedingung), dann werden die Informationen nur 
            # den Listen der Teilumläufe hinzugefügt.
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

                TeilumlaufDistanz.append(distance)
                Distanz.append(TeilumlaufDistanz)
                TeilumlaufDistanz = []

            else:
                PartDif.append(difTime)
                PartFromHS.append(fromhs)
                PartToHS.append(tohs)
                PartStartTime.append(stTime)
                PartEndTime.append(eTime)
                Teilumlauf.append(elementID)
                TeilumlaufDistanz.append(distance)
    
    # Am Ende werden die Listen den Dictionaries hinzugefügt, mit denen im Anschluss in der Simulation weitergearbeitet wird.
    DriveDuration_dic.update({i - 1: DifTime})
    FromHS_dic.update({i - 1: FromHS})
    ToHS_dic.update({i - 1: ToHS})
    PartStartTime_dic.update({i - 1: StartTime})
    PartEndTime_dic.update({i - 1: EndTime})
    ElementID_dic.update({i - 1: Umlauf})
    Distance_dic.update({i - 1: Distanz})


# **************** Datenbereinigung *********

# Die Daten weisen einige Fehler auf, in der Form, dass gelegentlich Teilumläufe
# nicht zeitlich geordnet sind. Das heißt es kommt vor, dass bspw. Teilumlauf 2
# vor Teilumlauf 1 in den Daten auftritt. Um dem entgegenzuwirken, wird im Folgenden
# einmal durch die gesamten Daten durchiteriert und mittels Insertion Sort die Teilumläufe
# richtig geordnet.
    
for i in range(0, len(numberVeh)):
    if (len(PartStartTime_dic[i])) > 1:
        for k in range(1, len(PartStartTime_dic[i])):
                
                key = PartStartTime_dic[i][k]
                key2 = DriveDuration_dic[i][k]
                key3 = PartEndTime_dic[i][k]
                key4 = FromHS_dic[i][k]
                key5 = ToHS_dic[i][k]
                key6 = ElementID_dic[i][k]
                key7 = Distance_dic[i][k]
                key8 = StartTime_dic[i][k]
              
                j = k-1
                while j >= 0 and key[0] < StartTime_dic[i][j] : 
                        PartStartTime_dic[i][j + 1] = PartStartTime_dic[i][j]
                        DriveDuration_dic[i][j + 1] = DriveDuration_dic[i][j] 
                        PartEndTime_dic[i][j + 1] = PartEndTime_dic[i][j] 
                        FromHS_dic[i][j + 1] = FromHS_dic[i][j] 
                        ToHS_dic[i][j + 1] = ToHS_dic[i][j] 
                        ElementID_dic[i][j + 1] = ElementID_dic[i][j] 
                        Distance_dic[i][j + 1] = Distance_dic[i][j] 
                        StartTime_dic[i][j + 1] = StartTime_dic[i][j] 
                        j -= 1
                PartStartTime_dic[i][j + 1] = key
                DriveDuration_dic[i][j + 1] = key2
                PartEndTime_dic[i][j + 1] = key3 
                FromHS_dic[i][j + 1] = key4 
                ToHS_dic[i][j + 1] = key5 
                ElementID_dic[i][j + 1] = key6 
                Distance_dic[i][j + 1] = key7 
                StartTime_dic[i][j + 1] = key8 


print("********* Dateneinleseroutine abgeschlossen. Daten in Dictionaries übertragen *******")


###############################################################################
################## Funktionen und Störungsgeneratoren #########################
###############################################################################

# Abfrage, ob Fahrtzeit über Simulationsdauer (Ist in diesem Fall auf einen Tag gesetzt)
def drive_outOfTime(time, clock):
    doOT = time + clock > 1440
    return doOT

# Falls die Zeit innerhalb des Berufsverkehrs ist, return true, sonst false.
def rushhour(time):
    if time >= RushhourStart1 and time <= RushhourEnde1:  # Fahrtzeit liegt in RushHour
        return True
    elif time >= RushhourStart2 and time <= RushhourEnde2:
        return True
    else:
        return False

# Die weather Funktion gibt die kummulierte Verspätung der Störungen "Regen" und "Sturm" aus.
# Sind Sturm und Regen in der GUI angeklickt worden, wird eine Verspätung errechnet, ansonsten nicht.
# Die Variable "delayType" ist nur notwendig, damit im Output der Simulation zu erkennen ist,
# welche Störung gerade aufgetreten ist.
# Durch die random.uniform Funktionen, werden Prozentwerte zwischen dem im Interface angegebenen
# Minimum und Maximum erzeugt. Hier können auch andere Verteilungsfunktionen angewendet werden,
# als die vorliegende Gleichverteilung. Mittels der zufällig erzeugten Wahrscheinlichkeiten wird
# die "delayCalculator" Funktion aufgerufen, die die eigentliche Verspätung berechnet.
def weather(driveduration):
    delay = 0
    delayType = ""
    if varSturm.get() == 1:  # Störungen durch Sturm
        wktSturm = round(random.uniform(wktSturm_Min, wktSturm_Max), 1)
        delaySturm = round(random.uniform(delaySturm_Min, delaySturm_Max), 1)
        delayactiveS = delayCalculator(wktSturm, driveduration, delaySturm)
        delay += delayactiveS
        if delayactiveS > 0:
            delayType += "|Sturm|"
    if varRegen.get() == 1:  # Störungen durch Regen
        wktRegen = round(random.uniform(wktRegen_Min, wktRegen_Max), 1)
        delayRegen = round(random.uniform(delayRegen_Min, delayRegen_Max), 1)
        delayactiveR = delayCalculator(wktRegen, driveduration, delayRegen)
        delay += delayactiveR
        if delayactiveR > 0:
            delayType += "|Regen|"
    return delay, delayType

# Diese Funktion berechnet die Verspätung für die Störung Wetter (siehe weather Methode)
# Hierfür wird die Wahrscheinlichkeit des Auftretens (Ausmaß) übernommen und mit dieser
# Wahrscheinlichkeit eine virtuelle Münze geworfen. Erzeugt die Münze eine 1, entsteht
# eine Verspätung, ansonsten nicht.
def delayCalculator(ausmaß, driveduration, delayonTop):
    delayperDisruption = 0
    coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
    if (coin == 1):
        delayperDisruption = int(driveduration * delayonTop)
    return delayperDisruption

# Falls die Starthaltestelle oder Endhaltestelle eine Haltestelle ist, an der eine Veranstaltung stattfindet,
# return true, sonst false.
def event(startHS, endHS, time):
    if (startHS in eventOrte or endHS in eventOrte):
        if (time >= eventStarttime and time <= eventEndtime):
            return True
        else:
            return False
    else:
        return False

# Diese Funktion errechnet eine Verspätung, sofern die BaustellenListe, welche durch eine Eingabe
# in der GUI erzeugt wird, die Start- bzw. Endhaltestelle der Fahrt eines Fahrzeuges inkludiert.
# Wie bei allen Störungsmustern werden auch hier die eigentliche Verspätung und die Verspätungsart
# zurückgegeben.
# Diese Methode wird im eigentlichen Störungsgenerator weiter unten aufgerufen.
def baustelle(startHS, endHS):
    if startHS in BaustellenListe or endHS in BaustellenListe:
        delayonTop = random.randint(delayBaustelle_Min, delayBaustelle_Max)
        delayType = "|Baustelle|"
    else:
        delayonTop = 0
        delayType = ""
    return delayonTop, delayType

# Diese Funktion errechnet eine Verspätung, sofern die SperrungListe, welche durch eine Eingabe
# in der GUI erzeugt wird, die Start- bzw. Endhaltestelle der Fahrt eines Fahrzeuges inkludiert.
# Wie bei allen Störungsmustern werden auch hier die eigentliche Verspätung und die Verspätungsart
# zurückgegeben.
# Diese Methode wird im eigentlichen Störungsgenerator weiter unten aufgerufen.
def sperrung(startHS, endHS, driveduration):
    if startHS in SperrungListe or endHS in SperrungListe:
        delaySperrung = round(random.uniform(delaySperrung_Min, delaySperrung_Max), 1)
        delayonTop = int(driveduration * delaySperrung)
        delayType = "|Sperrung|"
    else:
        delayonTop = 0
        delayType = ""
    return delayonTop, delayType

# Falls eine Fahrt eine Leerfahrt ist und ein Fahrzeug verspätet ist, dann sorgt diese
# Funktion dafür, dass das Fahrzeug schneller fährt (Dies spiegelt die Annahme wieder,
# dass ein Fahrzeug ohne Passagiere und Stops schneller fahren kann). Um wie viel % ein Fahrzeug
# schneller fährt, kann ebenso im Interface eingestellt werden.
def leerfahrt(delay, driveduration, elementtype):
    delayType = ""
    currentDelay = 0
    if delay > 0 and elementtype == 2:
        currentDelay = int(round(driveduration * avgPaceIncrease))
        if delay - currentDelay < 0:
            currentDelay = delay
        delayType = "|Leerfahrt|"
    else:
        delayType = ""
        currentDelay = 0
    return currentDelay, delayType


# Diese Funktion errechnet eine Verspätung, sofern die Liste unfallOrt, welche durch eine Funktion weiter
# unten erzeugt wird, die Start- bzw. Endhaltestelle der Fahrt eines Fahrzeuges inkludiert. Wie bei allen
# Störungsmustern werden auch hier die eigentliche Verspätung und die Verspätungsart zurückgegeben. 
# Diese Unfälle treten allerdings nur eine gewisse Zeit auf, die ebenso weiter unten generiert wird. Die
# maximale/minimale Zeitspanne eines Staus kann im Interface festgelegt werden.
# Diese Methode wird im eigentlichen Störungsgenerator weiter unten aufgerufen.
def unfall(startHS, endHS, driveduration, time):
    delay = 0
    delayType = ""
    if startHS in unfallOrt or endHS in unfallOrt:
        i = 0
        while i <= len(unfallOrt)-1:
            if startHS == unfallOrt[i] or endHS == unfallOrt[i]:
                if time >= unfallBeginn[i] and time < unfallEnde[i]:
                    delayonTop = round(random.uniform(delayStau_Min, delayStau_Max),1)
                    delay = int(driveduration * delayonTop)
                    delayType = "|Unfall|"
                    i += 1000
                else:
                    i += 1
            else:
                i += 1
    return delay, delayType

# Funktionen zur Unfallsimulation: Dies besteht aus mehreren einzelnen Funktionen

# 1. Unfallfunktion: Diese Funktion spiegelt den Punkt wider, dass Unfälle an verschiedenen
# Orten verschieden lang dauern. In der Innenstadt dauern Staus durch Unfälle durchschnittlich
# länger. Hier werden Unfälle zufällig einer von 3 "Staugruppen" zugeordnet.
def unfallzeitGroup():
    staugroup = numpy.random.choice(numpy.arange(0, 3), p=[0.1, 0.25, 0.65])
    return staugroup

# Quelle von def choice und def spaced_choice: https://stackoverflow.com/questions/47950131/drawing-random-numbers-with-draws-in-some-pre-defined-interval-numpy-random-ch/47950676
# 2. Unfallfunktion:
def choice(low, high, delta, n_samples):  # delta = wieviel abstand zwischen den Werten
    draw = numpy.random.choice(high - low - (n_samples - 1) * delta, n_samples, replace=False)
    idx = numpy.argsort(draw)
    draw[idx] += numpy.arange(low, low + delta * n_samples, delta)
    return draw

# 3. Unfallfunktion:
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

# 4. Unfallfunktion:
def flatList(list):
    flat_list = []
    for sublist in list:
        for item in sublist:
            flat_list.append(item)
    return flat_list

# 5. Unfallfunktion:
# Diese Funktion wird durch die Funktion unfallGenerator aufgerufen und ermittelt die
# verschiedenen Endzeiten der n Unfälle.
def unfallEndzeitCalculator(list):
    unfallEndzeiten = []
    for item in range(len(list)):
        stauDauer = random.randint(staudauerMin, staudauerMax)
        stauEndzeit = list[item] + stauDauer
        unfallEndzeiten.append(stauEndzeit)
    return unfallEndzeiten

# 6. Unfallfunktion:
# Diese Funktion wird durch die Funktion unfallGenerator aufgerufen und ermittelt die
# verschiedenen Startzeiten der n Unfälle.
def unfallStartzeitCalculator(n):
    unfallStartzeiten = []
    unfallgroups = [0, 0, 0]
    for i in range(n):
        unfallgroups[unfallzeitGroup()] += 1
    for i in range(len(unfallgroups)):
        unfallStartzeiten.append(spaced_choice(i, unfallgroups[i]))
    unfallStartzeiten = flatList(unfallStartzeiten)
    return unfallStartzeiten

# 7. Unfallfunktion:
# Diese Funktion ermittelt zufällig n verschiedene Haltestellen, an denen die Unfälle auftreten.
def unfallOrtCalculator(n):
    stauOrte = []
    for i in range(n):  ##Anzahl an Haltestellen mit Stau
        x = numpy.random.choice(df.FromStopID)
        stauOrte.append(x)
    return stauOrte

# 8. Unfallfunktion:
# Diese Funktion löst die vorherigen Funktionen aus und gibt am Ende sowohl 3 Listen mit 
# jeweils der Länge n aus. Die Liste "unfallBeginn" beinhaltet für jeden Unfall die Uhrzeit des jeweiligen
# Beginns. Die Liste "unfallEnde" beinhaltet für jeden Unfall die Uhrzeit des jeweiligen Endes. Die Liste "unfallOrt"
# gibt die Haltestellen an, an denen die Unfälle jeweils auftreten. 
def unfallGenerator(n):
    stauBeginn = unfallStartzeitCalculator(n)
    stauEnde = unfallEndzeitCalculator(stauBeginn)
    stauOrt = unfallOrtCalculator(n)
    return stauBeginn, stauEnde, stauOrt
unfallBeginn, unfallEnde, unfallOrt = unfallGenerator(anzahlUnfaelle)  # anzahlUnfaelle
unfallBeginn = list(unfallBeginn)
unfallEnde = list(unfallEnde)
unfallOrt = list(unfallOrt)


# 1. Störgenerator: passengerDisruption (wird durch die Simulation selbst aufgerufen)
# Diese Funktion ruft die oben zuvor beschriebenen Störungsmuster unter bestimmten Bedingungen auf.
# So wird etwa die Störung "Berufsverkehr" nur aufgerufen, wenn es sich um Elementtyp 1 (Servicefahrt)
# handelt, wenn im Interface der Berufsverkehr "angeschaltet" ist, und wenn sich die Zeit, in der diese
# Funktion aufgerufen wird, in der Berufsverkehrszeit befindet.
# Dieser Störungsgenerator verlängert die Haltezeiten um einen gewissen Wert.

def passengerDisruption(time, driveduration, startHS, endHS, elementtype):  # Funktion für die Verlängerung der Haltezeit
    delay = 0
    delayType = ""
    if elementtype == 1:
        if varRushhour == 1:
            if rushhour(time):
                delay += random.randint(delayRushhour_Halt_Min,delayRushhour_Halt_Max)
                delayType += "|Hauptverkehrszeit|"
        if varWeather == 1:
            delayWeather, delayTypeWeather = weather(driveduration)
            delay += delayWeather
            delayType += delayTypeWeather
        if varEvent == 1:
            if event(startHS, endHS, time):
                delayEvent_Halt = random.randint(delayEvent_Halt_Min, delayEvent_Halt_Max)
                delay += delayEvent_Halt
                delayType += "|Event|"
    return delay, delayType

# 2. Störgenerator: trafficDisruption (wird durch die Simulation selbst aufgerufen)
# Diese Funktion ruft die oben zuvor beschriebenen Störungsmuster unter bestimmten Bedingungen auf.
# Einige Störungsmuster treten sowohl in dieser, als auch im oberen Störungsgenerator auf, da beispielsweise
# der Berufsverkehr oder ein Event sowohl Haltezeiten als auch Fahrtzeiten beeinträchtigen.
# Dieser Störungsgenerator verlängert die Fahrtzeiten um einen gewissen Wert. Die einzelnen Störungsmuster
# folgen immer dem gleichen Prinzip, weshalb dem Störungsgenerator relativ simpel weitere Störungsmuster
# hinzugefügt werden können. 
# Ebenso wird hier die Funktion "leerfahrt" aufgerufen, wenngleich diese keine Störung hervorruft, aber dennoch
# dem gleichen Muster folgt.
def trafficDisruption(startHS, endHS, driveduration, time, elementtype):
    delay = 0
    delayType = ""
    if varRushhour == 1:
        if rushhour(time):
            delayRushhour = round(random.uniform(delayRushhour_Min, delayRushhour_Max),1)
            delay += int(delayRushhour * driveduration)
            delayType += "|Hauptverkehrszeit|"
    if varWeather == 1:
        delayWeather, delayTypeWeather = weather(driveduration)
        delay += delayWeather
        delayType += delayTypeWeather
    if varEvent == 1:
        if event(startHS, endHS, time):
            delayEvent = round(random.uniform(delayEvent_Min, delayEvent_Max),1)
            delay += int(delayEvent * driveduration)
            delayType += "|Event|"
    if varBaustelle == 1:
        delayBau, delayTypeBau = baustelle(startHS, endHS)
        delay += delayBau
        delayType += delayTypeBau
    if varSperrung == 1:
        delaySperrung, delayTypeSperrung = sperrung(startHS, endHS, driveduration)
        delay += delaySperrung
        delayType += delayTypeSperrung
    if varUnfall == 1 and varUnfallGUI.get() == 1:
        delayUnfall, delayTypeUnfall = unfall(startHS, endHS, driveduration, time)
        delay += delayUnfall
        delayType += delayTypeUnfall
    if varLeerfahrt == 1:
        delayLeerfahrt, delayTypeLeerfahrt = leerfahrt(delay, driveduration, elementtype)
        delay -= delayLeerfahrt
        delayType += delayTypeLeerfahrt
    return delay, delayType

# Funktion zur Nutzung der Pausen- und Wartezeit zum Abbau von Verspätungen
# Diese Funktion wird in der Simulation direkt aufgerufen. Hierbei wird zunächst überprüft,
# ob die Pufferzeiten zum Abbau genutzt werden sollen (varPufferzeit == 1). Falls ja, wird
# überprüft, ob es sich um Elementtyp 9 (Pufferzeiten) handelt. Ist das der Fall, wird die
# Pufferzeit so weit verkürzt, bis die Verspätung wieder 0 ist, bzw. bis die Pufferzeit komplett
# aufgebraucht ist. Das gleiche Vorgehen wird auch für die Pausenzeit gemacht.
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
    if varPausenzeit == 1:
        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 8:
            DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] = \
                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] - delayTime
            if DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] < 0:
                delayTime = abs(DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer])
                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] = 0
            else:
                delayTime = 0
    return delayTime

# Text für Konsole 
print("Simulation wurde gestartet...")
if (varUnfall == 1 and varUnfallGUI.get() == 1):
    print("Unfälle an folgenden Orten und Uhrzeit:", file=open("Output.txt", "a"))
    for i in range(0, len(unfallOrt)):
        print("Unfallort:", unfallOrt[i], " Zeitpunkt:", unfallBeginn[i], " Ausgelöst um:", unfallEnde[i], file=open("Output.txt", "a"))
    print("")

# Hier werden Variablen für die Kennzahlen initialisiert:
    
# Pünktlichkeit
global count_abfahrten
count_abfahrten = 0
global count_puenktlichAb
count_puenktlichAb = 0
global count_ankuenfte
count_ankuenfte = 0
global count_puenktlichAn
count_puenktlichAn = 0

# Wirkungsgrade
global count_Servicefahrten
count_Servicefahrten = 0
global count_Fahrten
count_Fahrten = 0

# Verspätungspropagation
global VP
VP = 0
global counterVP
counterVP = 0

columnsVP = ['Fahrzeug','Umlauf','VP']
VP_df = pd.DataFrame(columns = columnsVP)

# Verteilung Pufferzeiten
counterPausenzeit = 0

columnsPausenzeit = ['Fahrzeug','Umlauf','Haltestelle', 'Pausenzeit', 'Dauer Pufferzeit', 'Haltestellen gesamt']
Pausenzeit_df = pd.DataFrame(columns = columnsPausenzeit)
for i in range(len(ElementID_dic)):
    for j in range(len(ElementID_dic[i])):
        for k in range(len(ElementID_dic[i][j])):
            if ElementID_dic[i][j][k] == 9 or ElementID_dic[i][j][k] == 8:
                Pausenzeit_df.loc[counterPausenzeit] = [i+1,j+1,k+1,1, DriveDuration_dic[i][j][k],len(ElementID_dic[i][j])]
                counterPausenzeit += 1
            else:
                Pausenzeit_df.loc[counterPausenzeit] = [i+1,j+1,k+1,0, 0, len(ElementID_dic[i][j])]
                counterPausenzeit +=1
export_csv = Pausenzeit_df.to_csv(r'Verteilung Pausenzeiten.csv', index=None, header=True)

# Daten für CSV-Datei

print(
    "vehID Teilumlaufnummer Standort Dep/Arr Uhrzeit(Soll) Uhrzeit(Ist) Fahrtverspätung Gesamtverspätung Verspätungsursache",
    file=open("Q1.csv", "a"))

# Objekt Vehicle für die Simulation, die weiter unten gestartet wird
def vehicle(env, vehID):    # Eigenschaften von jedem Fahrzeug; folgender Code wird für jedes Fahrzeug einzeln ausgeführt
    while True:             # Solange die Uhrzeit <= 1440 ist, läuft diese Schleife. Wird unten durch "except" abgebrochen.
        for teilumlaufnummer in range(0, len(StartTime_dic) - 1):  # Loop der durch die einzelnen Teilumläufe führt
            global VP
            VP = 0
            try:
                if StartTime_dic[vehID][teilumlaufnummer] - env.now >= 0:   # Bedeutet, dass die Startzeit zu diesem Zeitpunkt noch nicht erreicht ist
                    delayTime = 0
                    yield env.timeout(
                        StartTime_dic[vehID][teilumlaufnummer] - env.now)   # Timeout für Fahrzeug solange, bis Startzeit erreicht. (Solange ist Objekt Fahrzeug inaktiv)
                else:
                    yield env.timeout(0)
                    delayTime = env.now - StartTime_dic[vehID][teilumlaufnummer]

                umlaufstatus = 1  # Wenn Startzeit erreicht, Fahrzeug im Umlauf (umlaufstatus = 1)

                while umlaufstatus == 1:  # solange das Fahrzeug im Umlauf ist, wird Folgendes ausgeführt:
                    for fahrtnummer in range(0, len(FromHS_dic[vehID][teilumlaufnummer])): # Iteration durch jede einzelne Fahrt

                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9 or ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 8: 
                            fahrtstatus = "Pause"                               # Wenn Elementtyp 8/9 (Pause/Puffer)ist, kann keine Verspätung entstehen             
                            delayPassenger = 0                                  # Status wird für den Output auf Pause gesetzt
                            delayTypePassenger = "|---|"
                        else:
                            fahrtstatus = 0  # 0 = Abfahrt / 1 = Ankunft / 2 = Pause
                            # Verspätungen durch Haltezeit: Ist diese Fahrt kein Elementtyp 8/9, dann wird der Störungsgenerator "passengerDisruption" aufgerufen (Siehe oben)
                            delayPassenger, delayTypePassenger = passengerDisruption(env.now,
                                                                                     DriveDuration_dic[vehID][
                                                                                         teilumlaufnummer][fahrtnummer],
                                                                                     FromHS_dic[vehID][
                                                                                         teilumlaufnummer][fahrtnummer],
                                                                                     ToHS_dic[vehID][teilumlaufnummer][
                                                                                         fahrtnummer],ElementID_dic[vehID][teilumlaufnummer][fahrtnummer])

                        delayTime_perStop = delayPassenger
                        delayType = delayTypePassenger

                        delayTime += delayTime_perStop # Der Gesamtverspätung wird die Einzelverspätung aufsummiert
                        yield env.timeout(delayTime_perStop) # Timeout bedeutet, dass das Fahrzeug die nächste Fahrt erst antreten kann,
                                                            # wenn die errechnete Haltezeitverspätung vorüber ist.

                        # Kennzahl: Pünktlichkeit (Abfahrt)
                        verspaetung = env.now - PartStartTime_dic[vehID][teilumlaufnummer][fahrtnummer]
                        global count_abfahrten
                        count_abfahrten += 1
                        if verspaetung == 0:
                            global count_puenktlichAb
                            count_puenktlichAb += 1
                        
                        # Das Ereignis "Haltezeit" ist nun abgeschlossen und wird in den Output mit allen relevanten Parametern übergeben. 
                        print(vehID + 1, teilumlaufnummer + 1, FromHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                              fahrtstatus, PartStartTime_dic[vehID][teilumlaufnummer][fahrtnummer], env.now,
                              delayTime_perStop, delayTime, delayType,
                              file=open("Q1.csv", "a"))

                        # Nachdem die Haltezeit abgeschlossen ist und die Fahrt beginnt, wird nun diese simuliert und eine mögliche Verspätung berechnet
                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:    #Sofern es sich nicht um eine Fahrt, sondern um eine Pufferzeit handelt, wird der 
                            delayTime_perDrive = 0                                      # Störungsgenerator "trafficDisruption" nicht aktiviert.
                            delayType = "|---|"
                        else:
                            delayTraffic, delayTypeTraffic = trafficDisruption(         # Handelt es sich jedoch nicht um eine Pufferzeit, wird der Störungsgenerator hier aktiviert.
                                FromHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer],
                                env.now, ElementID_dic[vehID][teilumlaufnummer][fahrtnummer])

                            delayTime_perDrive = delayTraffic
                            delayType = delayTypeTraffic

                        # Aufsummieren der Verspätungen im Teilumlauf (gleiches Schema wie bei Haltezeitverspätung)
                        delayTime += delayTime_perDrive

                        # Abfrage, ob Fahrt innerhalb der Simulationszeit liegen würde; falls nicht, wird die Simulation für dieses Fahrzeug abgebrochen, andernfalls wird es ausgeführt.
                        if drive_outOfTime(
                                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer], env.now):
                            yield env.timeout(1440)
                            break

                        # Hier wird die oben beschriebene breaktime Funktion ausgeführt, die eine mögliche Nutzung der Puffer-/ Pausenzeiten berechnet.
                        delayTime = breaktime(vehID, teilumlaufnummer, fahrtnummer, delayTime)
                        
                        # Für die KPI Verspätungspropagation wird hier die Verspätungszeit aufsummiert
                        VP += delayTime

                        # Das Fahrzeug erhält wieder einen Timeout, das heißt, für diese Zeit kann das Fahrzeug keine neuen Aktivitäten starten (die nächste Fahrt antreten)
                        yield (
                            env.timeout(DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] + delayTime_perDrive))

                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            fahrtstatus = "Pause"
                        else:
                            fahrtstatus = 1
                        
                        # Kennzahl: Wirkungsgrad
                        global count_Fahrten  # Aufsummierung der Fahrzeit aller Fahrten
                        count_Fahrten += (DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] + delayTime)
                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 1:
                            global count_Servicefahrten  # Aufsummierung der Fahrzeit aller Servicefahrten
                            count_Servicefahrten += (DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] + delayTime)
                        
                        
                        # Kennzahl: Pünktlichkeit (Ankunft)
                        verspaetung = env.now - PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer]
                        global count_ankuenfte
                        count_ankuenfte += 1
                        if verspaetung == 0:
                            global count_puenktlichAn
                            count_puenktlichAn += 1

                        # Die Fahrt ist abgeschlossen und das Ereignis wird mit allen relevanten Attributen in den Output übernommen.
                        # Ebenso Abfrage ob Bus im Depot angekommen: Falls ja, wird Umlaufstatus auf 0 gesetzt und der Teilumlauf ist beendet. 
                        # Dann ist die oben begonnene While-Schleife beendet und der nächste Teilumlauf kann stattfinden.
                        if ToHS_dic[vehID][teilumlaufnummer][fahrtnummer] == DepotID[vehID]:
                            print(vehID + 1, teilumlaufnummer + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  fahrtstatus, PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  env.now, delayTime_perDrive, delayTime, delayType,
                                  file=open("Q1.csv", "a"))
                            umlaufstatus = 0
                        else:
                            print(vehID + 1, teilumlaufnummer + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  fahrtstatus, PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  env.now, delayTime_perDrive, delayTime, delayType,
                                  file=open("Q1.csv", "a"))
                # Relevant für KPI Verspätungspropagation: die FahrzeugID, die Teilumlaufnummer und der Wert der Verspätungs-
                # propagation werden in das entsprechende Dataframe übernommen.
                global counterVP
                VP_df.loc[counterVP] = [vehID + 1, teilumlaufnummer + 1, VP]
                counterVP += 1
            except:
                if env.now >= 1440:  # to avoid RunTimeError: GeneratorExit
                    return False
                continue



# Simulationsumgebung 
env = simpy.Environment()

# Initialisierung von Fahrzeugen
for i in range(0, len(numberVeh)):  # Anzahl von Fahrzeugen = len(numberVeh)
    env.process(vehicle(env, i))  # Inputdaten Eigenschaften Fahrzeugen
# Simulation starten und Laufzeit festlegen
env.run(until=1440)  # Ein Tag simulieren: in Minuten ausdrücken. 24h = 1440min


# Ausgabe von Kennzahlen 
print("~~~~~~~~~~~ Kennzahlen ~~~~~~~~~~~~~", file=open("Output.txt", "a"))
print("***Pünktlichkeit***", file=open("Output.txt", "a"))
print("Anzahl Abfahrten: ", count_abfahrten, " davon pünktlich: ", count_puenktlichAb, file=open("Output.txt", "a"))
print("Anzahl Ankünfte: ", count_ankuenfte, " davon pünktlich: ", count_puenktlichAn, file=open("Output.txt", "a"))
print("***Wirkungsgrade***", file=open("Output.txt", "a"))
print("Anzahl Fahrten (total): ", count_Fahrten, " davon Servicefahrten: ", count_Servicefahrten, file=open("Output.txt", "a"))
export_csv = VP_df.to_csv(r'VP.csv', index=None, header=True)