# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 14:39:05 2019

@author: svenr
"""

# Sprint2.3
# Neuerungen:
# - dispositive Abfrage rausgenommen
# - vehID in Schleife korrigiert, übersichtlicher gestaltet

# ToDos:
# - Komplexere Abhängigkeiten (Break/Add)
# - Störungsmuster
# - Fahrer (DutyID) einbauen


####################### Import Packages ###################################
import simpy
import pandas as pd
import numpy

####################### Daten einlesen ####################################
df = pd.read_csv("tableFinal.csv", sep=";")
# df.info()

####################### Daten transformieren (Zeit) ########################
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

# Gesamtanzahl an Fahrzeugen ermitteln
numberVeh = df["BlockID"].unique()
numberVeh = numberVeh.tolist()  # von Array in Liste formatieren
numberVeh = [elem for elem in numberVeh if elem >= 0]  # -1 entfernen
print("Die Gesamtanzahl von Fahrzeugen beträgt %d." % len(numberVeh))

# DepotID (jedem Fahrzeug die unique DepotID zuordnen
DepotID = []
counter = 1
for i in range(1, len(numberVeh) + 1):
    for j in range(0, df.shape[0]):
        if df.BlockID[j] == i and counter == i:
            DepotID.append(df.DepotID[j])
            counter += 1
print("Jedes Fahrzeug besitzt eine DepotID: %s" % (
        len(DepotID) == len(numberVeh)))  # Frage: Hat jedes Fahrzeug nur ein Depot oder kann das wechseln??

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
    startTime_dic.update({(i-1): startTimes_Block}) #i-1 damit Index bei 0 anfängt (wichtig für Schleife (nachträgliche Änderung!)

StartTime_dic = startTime_dic
StartTime_dic
print("Jedes Fahrzeug fährt mindestens einmal aus dem Depot: %s" % (len(StartTime_dic) == len(numberVeh)))

stopTime_dic = {}
for i in range(1, len(numberVeh) + 1):
    stopTimes_Block = []
    for j in range(len(df)):
        if df.BlockID[j] == i:
            if df.ToStopID[j] == DepotID_plusOne[i]:
                stopTimes_Block.append(df.EndTime[j])
    stopTimes_Block = stopTimes_Block + [1440]  # Add to every list a 1440 as last element for simulation loop (timeout)
    stopTime_dic.update({(i-1): stopTimes_Block}) #i-1 damit Index bei 0 anfängt (wichtig für Schleife (nachträgliche Änderung!)
    

StopTime_dic = stopTime_dic


# Listen von Haltestellen (from/to) (Liste mit vielen Listen)
FromStopID = []
ToStopID = []
for i in range(1, len(numberVeh) + 1):
    fromStopID_cache = []
    toStopID_cache = []
    for j in range(0, df.shape[0]):
        if df.BlockID[j] == i:
            fromStopID_one = df.iloc[j, 3]
            fromStopID_cache.append(fromStopID_one)
            toStopID_one = df.iloc[j, 4]
            toStopID_cache.append(toStopID_one)
    FromStopID.append(fromStopID_cache)
    ToStopID.append(toStopID_cache)
print("Die Anzahl der StoppointListen (from) ist gleich der Anzahl der Fahrzeuge: %s." % (
        len(FromStopID) == len(numberVeh)))
print(
    "Die Anzahl der StoppointListen (to) ist gleich der Anzahl der Fahrzeuge: %s." % (len(ToStopID) == len(numberVeh)))

# Fahrzeit zwischen den einzelnen Stationen (einfache Liste)
DriveDuration = []
for i in range(1, len(numberVeh) + 1):
    DifTime = []
    for j in range(0, df.shape[0]):
        if df.BlockID[j] == i:
            difTime = df.iloc[j, 12] - df.iloc[j, 13]
            DifTime.append(difTime)
    DriveDuration.append(DifTime)
print(
    "Die Anzahl der Fahrtzeitlisten ist gleich der Anzahl der Fahrzeuge: %s." % (len(DriveDuration) == len(numberVeh)))

DelayedStartTime = []
DelayedEndTime = []
for x in range(0, count_row):
    DelayedStartTime.append(0)
    DelayedEndTime.append(0)
df["DelayedStartTime"] = DelayedStartTime
df["DelayedEndTime"] = DelayedEndTime

###Add number of partblock###
PartBlock = []
for x in range(0, count_row):
    PartBlock.append(0)
df["PartBlock"] = PartBlock


for y in range(1, 100):
    counter = 1
    for x in range(0, count_row):
        if df.iloc[x,1] == -1:
            df.iloc[x,16] = (df.iloc[x,1])
        if y == df.iloc[x,1]:
            df.iloc[x,16] = counter
            if df.iloc[x,4] > 160:
                counter += 1


DifTime = []
count_row = df.shape[0]
for x in range(0, count_row):
    difTime = df.iloc[x,12] - df.iloc[x,13]
    DifTime.append(difTime)

df["Duration"] = DifTime
############################## Daten, die für die Simulation benötigt werden, und deren Form #######################

# Spalten in Dataframe: StartTime und EndTime (in Minuten)
# Liste von der Gesamtanzahl von Fahrzeugen: numberVeh
# Liste von Depots, von denen eins einem Fahrzeug zugeordnet ist: DepotID
# Dictionary mit den Startzeiten jedes Teilumlaufs (Liste) von jedem Fahrzeug: StartTime_dic
# Liste von Listen mit den Haltestellen eines jeden Fahrzeugs (über alle Teilumläufe hinweg): FromStopID & ToStopID
# Liste von Listen mit den einzelnen Fahrtzeiten von der entsprechenden FromStopID zur entsprechen ToStopID: DriveDuration

numberVeh


############################## Funktionen für Objekt Vehicle #############################

def Störungsfaktor(y):
    ##randomisieren und nicht für alle Fahrten anwenden
    for x in range(0, count_row):
        df.iloc[x,14] = df.iloc[x,13] * y
        df.iloc[x,15] = df.iloc[x,12] * y
Störungsfaktor(1)


###Gibt die Zeit des letzten Umlaufs dieses Fahrzeugs zurück 
def TimeOfLastBlock(z):
    currentPartBlock = df.iloc[z,16]
    lastPartBlock = df.iloc[z,16] -1
    currentBlock = df.iloc[z,1]
    time = 0
    for x in range(0, count_row):
        if df.iloc[x,15] > time and df.iloc[x,16] == lastPartBlock and df.iloc[x,1] == currentBlock:
            time = df.iloc[x,15]
    return time
#df.iloc[2677,15] = 850

##Verschiebt die Zeit
def TimeShift(z):
    currentPartBlock = df.iloc[z,16]        ##Der wievielte Teilumlauf des Fahrzeugs ist es? 
    currentBlock = df.iloc[z,1]             ##Welches Fahrzeug ist es?
    if df.iloc[z,14] < TimeOfLastBlock(z):
        shift = TimeOfLastBlock(z) - df.iloc[z,14]
        df.iloc[z,14] += shift                      ##Ändert die Startzeit auf den frühestmögl. Punkt
        df.iloc[z,15] += shift                      ##Ändert die Endzeit
        for x in range(0, count_row):
            if df.iloc[x,16] == currentPartBlock and df.iloc[x,1] == currentBlock:##für alle einträge dieses Teilumlaufs
                if df.iloc[x-1,16] == currentPartBlock:     ##Nur wenn der vorherige Umlauf auch schon teil des Teilumlaufs war
                    df.iloc[x,14] = df.iloc[x-1,15]         ##Setze Startzeit der Fahrt auf die Endzeit der vorherigen Fahrt
                    df.iloc[x,15] = df.iloc[x,14] + df.iloc[x,17] ##Endzeit berechnet sich aus der Startzeit + Dauer
                if df.iloc[x,7] == 9 and shift > 0:         ##Wenn es eine Pause ist, wird die Pause nicht genutzt sondern direkt
                    shift -= df.iloc[x,17]                  ##weitergefahren um die Verschiebung wieder aufzuholen, bis verschiebung = 0
                    if shift < 0:
                        shift = 0
                    df.iloc[x,15] = df.iloc[x,14]           ##Setzt die dauer der Pause auf 0



# Abfrage: Fahrtzeit über Simulationsdauer
def drive_outOfTime(time, delay, clock):
    doOT = time + delay + clock >= 1440
    return doOT


# Störgenerator
def stoerfaktor(n):  # n = Eingabeparameter um Störausmaß zu steuern
    if (n == 0):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                              0.0])  # Wahrscheinlichkeiten von Störungen / für jeden
        # Teilfahrt neuen Störfaktor
    elif (n == 1):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.6, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                              0.0])  # Wahrscheinlichkeiten von Störungen / für jeden
        # Teilfahrt neuen Störfaktor
    elif (n == 2):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.6, 0.0, 0.0, 0.2, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0,
                                                              0.0])  # Wahrscheinlichkeiten von Störungen / für jeden
        # Teilfahrt neuen Störfaktor
    elif (n == 3):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.33, 0.0, 0.0, 0.0, 0.0, 0.33, 0.0, 0.0, 0.0, 0.0,
                                                              0.34])  # Wahrscheinlichkeiten von Störungen / für
        # jeden Teilfahrt neuen Störfaktor
    return factorX


############################## Daten für CSV-Datei ###############################
# Header für CSV-Datei
print("vehID Standort Dep/Arr Uhrzeit(Ist) Status(Depot/Umlauf)",
      file=open("TestDelayCSV.csv", "a"))

########################## Objekt Vehicle #########################################
def vehicle(env, vehID):  # Eigenschaften von jedem Fahrzeug
    while True:
        counter = 0
        delayTime = 0  # DelayTime initialisieren (gilt für den ganze Tag des Fahrzeugs)

        for j in range(0, len(StartTime_dic) - 1):  # Loop der durch die einzelnen Teilumläufe führt
            timeStartSection = StartTime_dic[vehID][j] - env.now  # Startzeit des jeweiligen Umlaufs
            yield env.timeout(timeStartSection)  # Timeout bis Start des Teilumlaufes
            status = 1  # Wenn Startzeit erreicht, Fahrzeug im Umlauf (Status = 1)

            while status == 1:  # while Fahrzeug im Umlauf
                cache_counter = 0  # wichtig, weil Start und EndHaltestellen in einer Liste, sodass counter
                # TeilumlaufHaltestellen abgrenzt
                askoneTime = 0  # Variable für InputTest User Fahrtabbruch
                for k in range(0, len(ToStopID[vehID])):

                    # Einstellen des Störfaktors
                    delayTime_perDrive = stoerfaktor(0)
                    delayTime = delayTime + delayTime_perDrive  # Aufsummieren der Verspätungen im Teilumlauf

                    # Event: Bus fährt um bestimmte Uhrzeit von HS los
                    itemDrive = 0  # Abfahrt = 0, Ankunft = 1
                    print(vehID+1, FromStopID[vehID][k + counter], itemDrive, env.now, status,
                          file=open("TestDelayCSV.txt", "a"))

                    # Abfrage, ob Fahrt außerhalb der Simulationszeit liegen würde
                    if drive_outOfTime(DriveDuration[vehID][k + counter], delayTime, env.now):
                        print(vehID+1, FromStopID[vehID][k + counter], itemDrive, env.now, 404,
                              file=open("TestDelayCSV.txt", "a"))
                        yield env.timeout(1440)
                        break

                    # Timeout für Fahrtdauer zur nächsten Haltestelle
                    yield (env.timeout(DriveDuration[vehID][k + counter] + delayTime))

                    # Event: Bus kommt zu bestimmter Uhrzeit an HS an
                    itemDrive = 1
                    # Abfrage ob Bus im Depot angekommen
                    if ToStopID[vehID][k + counter] == DepotID[vehID]:
                        status = 0
                        cache_counter += 1
                        print(vehID+1, DepotID[vehID], itemDrive, env.now, status,
                              file=open("TestDelayCSV.txt", "a"))
                        break
                    else:
                        print(vehID+1, ToStopID[vehID][k + counter], itemDrive, env.now, status,
                              file=open("TestDelayCSV.txt", "a"))
                        cache_counter += 1


            # Counter für Drive_DurationListe übertragen
            counter = counter + cache_counter

            # Abfrage ob AnschlussUmlauf erreicht wird
            if (StartTime_dic[vehID][j + 1] - env.now < 0):
                yield env.timeout(1440)
            else:
                yield env.timeout(abs(StartTime_dic[vehID][j + 1] - env.now))
                delayTime = 0  # gesammelten Verspätungen hatten keinen Impact auf weiterführende Teilumläufe (RESET)


########################## Simulationsumgebung ##############################
env = simpy.Environment()

# Initialisierung von Fahrzeugen
for i in range(0, len(numberVeh)):  # Anzahl von Fahrzeugen = len(numberVeh)+1
    env.process(vehicle(env, i))  # Inputdaten Eigenschaften Fahrzeugen
    # Problem: BlockID fängt bei 1 an. Alle Listen und Dictionarys fangen immer bei 0 an. Mismatch gelöst mit (-1)
# Simulation starten und Laufzeit festlegen
env.run(until=1440)  # Ein Tag simulieren: in Minuten ausdrücken. 24h = 1440min