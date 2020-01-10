####################### Import Packages ###################################
import simpy
import pandas as pd
import numpy
from random import randint
from tkinter import *


root = Tk()
root.geometry("400x500")
l0 = Label(root,text='Globale Einstellungen',background='grey', font = "Times")
varPassagieraufkommen = IntVar()
cPassagieraufkommen = Checkbutton(root, text='erhöhtes Passagieraufkommen an einigen Haltestellen',
                                  variable=varPassagieraufkommen)
varVerkehrsaufkommen = IntVar()
cVerkehrsaufkommen = Checkbutton(root, text='erhöhtes Verkehrsaufkommen an einigen Haltestellen',
                                  variable=varVerkehrsaufkommen)
varPufferzeit = IntVar()
cPufferzeit = Checkbutton(root, text='Pufferzeiten für Abbau von Verspätungen nutzen',
                                  variable=varPufferzeit)
l1 = Label(root,text='Verkehrslage',background='grey', font = "Times")
varUnfall = IntVar()
cUnfall = Checkbutton(root, text='Unfall nahe einer Haltestelle',
                      variable=varUnfall)
varBaustelle = IntVar()
cBaustelle = Checkbutton(root, text='Baustelle an bestimmter Haltestelle (hier: HS 29)',
                         variable=varBaustelle)
l2 = Label(root,text='Wetter',background='grey', font = "Times")
varSturm = IntVar()
cSturm = Checkbutton(root, text='An diesem Tag gibt es Sturm.',
                     variable=varSturm)
varRegen = IntVar()
cRegen = Checkbutton(root, text='An diesem Tag regnet es.',
                     variable=varRegen)
l3 = Label(root,text='Specials',background='grey', font = "Times")
varFahrzeugausfall = IntVar()
cFahrzeugausfall = Checkbutton(root, text='Fahrzeug fällt aus (1%)',
                               variable=varFahrzeugausfall)
button = Button(text = "Bestätigen", bg = "green", command = root.destroy)

l0.pack(fill=X, padx='20', pady='5')
cPassagieraufkommen.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
cVerkehrsaufkommen.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
cPufferzeit.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
l1.pack(fill=X, padx='20', pady='5')
cUnfall.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
cBaustelle.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
l2.pack(fill=X, padx='20', pady='5')
cSturm.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
cRegen.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
l3.pack(fill=X, padx='20', pady='5')
cFahrzeugausfall.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
button.pack(side='bottom', fill='y', padx='5',pady='10')

mainloop()

####################### Daten einlesen ####################################
df = pd.read_csv("/home/chris/PythonProjekte/SemProjekt-1920/tableFinal.txt", sep=";")
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

##für die Annahme, dass ein Stau eher im Zentrum ist (Annahme, dass Zentrum dort ist, wo eine Haltestelle stark befahren wird)
cumulativeHS = []
cumulative = 0
for j in range(0, len(HScount)):
    cumulative += HScount[j]
    cumulativeHS.append(cumulative)

##Random mit gewichteter Wahrscheinlichkeit 10 Haltestellen, an denen Stau entsteht
Jam = []
for i in range(0, 10):  ##Anzahl an Haltestellen mit Stau
    x = (randint(0, count_row))
    for j in range(0, len(cumulativeHS)):
        if x <= cumulativeHS[j]:
            Jam.append(j)
            break



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
    if varPassagieraufkommen.get() == 1: #Passagieraufkommen
        ausmaß = 0.2
        delayonTop = 0.2
        coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
        if (coin == 1):
            delay += int(driveduration * delayonTop)
            delayType += "PA"
    if varVerkehrsaufkommen.get() == 1: #Verkehrsaufkommen
        if fromhs in Jam or tohs in Jam:
            if (time < 390) or (time > 1200): # Schwachverkehrszeiten
                ausmaß = 1
                delayonTop = 0
                coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
                if (coin == 1):
                    delay += int(driveduration * delayonTop)
                    delayType += ", VA(Schwach)"
            if (time > 510 and time < 870) or (time > 1110 and time <= 1200): #Normalverkehrzeiten
                ausmaß = 0.5
                delayonTop = 0.1
                coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
                if (coin == 1):
                    delay += int(driveduration * delayonTop)
                    delayType += ", VA(Normal)"
            if (time >= 390 and time <= 510) or (time >= 870 and time <= 1110): # Hauptverkehrszeiten
                ausmaß = 1
                delayonTop = 0.4
                coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
                if (coin == 1):
                    delay += int(driveduration * delayonTop)
                    delayType += ", VA(Haupt)"
    if varSturm.get() == 1: #Sturm
        ausmaß = 0.8 # Anteil an Fahrten, die von Störung betroffen sind
        delayonTop = 0.6 # Verspätung, die abhängig von Fahrtzeit on Top auf die Fahrtzeit raufkommt
        coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
        if (coin == 1):
            delay += int(driveduration * delayonTop)
            delayType += ", Sturm"
    if varRegen.get() == 1: #Regen
        ausmaß = 0.5
        delayonTop += 0.4
        coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
        if (coin == 1):
            delay += int(driveduration * delayonTop)
            delayType += ", Regen"
    if varFahrzeugausfall.get() == 1:
        ausmaß = 0.01
        delayonTop += 1440
        coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
        if (coin == 1):
            delay += int(driveduration * delayonTop)
            delayType += ", Fahrzeugausfall"
    return delay, delayType #Type der Störung bei Ausgabe angeben (durch Input Checkbox bestimmt)(Funktion immer dieselbe)

BaustelleanbestimmterHS = [29] # Eingabe von Benutzer nutzen
def selectionDisruption(fromhs, tohs, driveduration, time):
    delay = 0
    delayType = ""
    if varBaustelle.get() == 1:
        if fromhs in BaustelleanbestimmterHS or tohs in BaustelleanbestimmterHS:
            ausmaß = 1
            delayonTop = 1
            coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
            if (coin == 1):
                delay += int(driveduration * delayonTop)
                delayType += ", Baustelle"
    if varUnfall.get() == 1:
        ausmaß = 0.05
        delayonTop = 1
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
# Header für CSV-Datei
print(
    "vehID Teilumlaufnummer Standort Dep/Arr Uhrzeit(Soll) Uhrzeit(Ist) Fahrtverspätung Gesamtverspätung Verspätungsursache",
    file=open("Eventqueue5.3-Chris.txt", "a"))


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
                              file=open("Eventqueue5.3-Chris.txt", "a"))

                        # Verspätung auf Fahrt ermitteln
                        delayType = ""
                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            delayTime_perDrive = 0
                            delayType = "-"
                        else:
                            delayGlobal, delayTypeGlobal = globalDisruption(DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer],
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
                                  file=open("Eventqueue5.3-Chris.txt", "a"))
                            umlaufstatus = 0
                        else:
                            print(vehID + 1, teilumlaufnummer + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  fahrtstatus, PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  env.now, delayTime_perDrive, delayTime, delayType,
                                  file=open("Eventqueue5.3-Chris.txt", "a"))

            except:
                if env.now >= 1440:  # to avoid RunTimeError: GeneratorExit
                    return False
                continue

            ########################## Simulationsumgebung ##############################


env = simpy.Environment()

# Initialisierung von Fahrzeugen
for i in range(0, 1):  # Anzahl von Fahrzeugen = len(numberVeh)
    env.process(vehicle(env, i))  # Inputdaten Eigenschaften Fahrzeugen
# Simulation starten und Laufzeit festlegen
env.run(until=1440)  # Ein Tag simulieren: in Minuten ausdrücken. 24h = 1440min
