# Sprint3.1

# vehID!!! eingefügt


# für Erhebung von KPI für Robustheit (Anzahl ausfallender Teilumläufe)

# funktionierende Version ohne Break-Bedingung und Überprüfung, ob einer der Teilumläufe erreicht werden kann

# ToDos (short view):
# - Simulation mit verschiedenen Parametern für Puffer, max. zu skippende HS, Fahrtzeit zum Depot ausführen
# - RobustheitsKPIs erheben mit Break-Bedinung und (!) ohne

# Neuerungen:
# - Dictionary mit Länge der einzelnen Teilumläufe jeden Fahrzeugs:
#        - Break-Bedingung besser zu realisieren
#        - ggf. möglich Loop umzubauen (counter & cache_counter raus)

# Ziel: Abhängigkeit von Teilumläufen einbauen durch Abbruchbedingung

# Idee:
# - Abfrage, wenn Startzeit des nächsten Umlaufes fast erreicht ist, aber der Umlauf noch nicht beendet ist:
#       + Wenn Anzahl der noch anzufahrenden HS vor Ankunft am Depot kleiner X, dann Abbruch des Umlaufs und
#           direkt zum Depot
#       + Fahrtzeit zum Depot von der HS dann erst versuchen aus Daten zu lesen oder Annahme machen
#           (Durchschnitt oder so)
#       + fast erreicht = Wenn Startzeit nächster Umlauf - env.now < 20min (oder anderer Wert),
#           dann Berechnung Fahrtzeit vor Abfahrt von jeder HS zum Depot (wenn < Starttime - env.now, dann Abbruch)

# Bei Durchführung Error in den Daten ausgefallen:
#   Bei VehID 9, 77, 63 sind die Teilumläufe nicht in korrekter Reihenfolge
#   Idee: Zeiten aufsteigend sortieren bei Transformieren


# ToDos:
# - komplexere Störmuster
# - Vorstudien mit Sprint2.1
# - Fahrer (DutyID) einbauen / Ressourcenabhängigkeit


####################### Import Packages ###################################
import simpy
import pandas as pd
import numpy

####################### Daten einlesen ####################################
df = pd.read_csv("/home/chris/PythonProjekte/SemProjekt-1920/tableFinal.txt", sep=";")
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
    startTime_dic.update(
        {(i - 1): startTimes_Block})  # i-1 damit Index bei 0 anfängt (wichtig für Schleife (nachträgliche Änderung!)

StartTime_dic = startTime_dic
StartTime_dic
print("Jedes Fahrzeug fährt mindestens einmal aus dem Depot: %s" % (len(StartTime_dic) == len(numberVeh)))

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
len(DriveDuration)

# Dictionaries mit Fahrzeug: [TeilumlaufHS][TeilumlaufHS]... + Länge der einzelnen Teilumläufe (nachträglich eingefügt)
lenTeilumlaeufe_dic = {}
FromHS_dic = {}
ToHS_dic = {}
for i in range(0, len(ToStopID)):
    lenTeil = []
    FromTeil = []
    ToTeil = []
    lencounter = 0
    for j in range(0, len(ToStopID[i])):
        if ToStopID[i][j] == DepotID[i]:
            lencounter += 1
            lenTeil.append(lencounter)
            lencounter = 0
            FromHS_dic.update({i: FromTeil})
            FromTeil = []
            ToHS_dic.update({i: ToTeil})
            ToTeil = []
        else:
            FromTeil.append(FromStopID[i])
            ToTeil.append(ToStopID[i])
            lencounter += 1
    lenTeilumlaeufe_dic.update({i: lenTeil})

lenTeilumlaeufe_dic[81]

len(DriveDuration)
DriveDuration_dic = {}
for i in range(0, len(DriveDuration)):
    driveAll = []
    driveTeil = []
    counterinList = 0
    k = 0
    for j in range(0, len(DriveDuration[i])):
        print(counter)
        if counterinList == (lenTeilumlaeufe_dic[i][k]) - 1:
            driveTeil.append(DriveDuration[i][j])
            driveAll.append(driveTeil)
            print(driveTeil)
            driveTeil = []
            counterinList = 0
            k += 1
        else:
            print("i: %d, j: %d" % (i, j))
            driveTeil.append(DriveDuration[i][j])
            counterinList += 1
    DriveDuration_dic.update({i: driveAll})

DriveDuration_dic


############################## Daten, die für die Simulation benötigt werden, und deren Form #######################

# Spalten in Dataframe: StartTime und EndTime (in Minuten)
# Liste von der Gesamtanzahl von Fahrzeugen: numberVeh
# Liste von Depots, von denen eins einem Fahrzeug zugeordnet ist: DepotID
# Dictionary mit den Startzeiten jedes Teilumlaufs (Liste) von jedem Fahrzeug: StartTime_dic
# Liste von Listen mit den Haltestellen eines jeden Fahrzeugs (über alle Teilumläufe hinweg): FromStopID & ToStopID
# Liste von Listen mit den einzelnen Fahrtzeiten von der entsprechenden FromStopID zur entsprechen ToStopID: DriveDuration
# Länge der einzelnen Teilumläufe in Dictionary mit Listen gespeichert


############################## Funktionen für Objekt Vehicle #############################

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
print("vehID Standort Dep/Arr Uhrzeit(Ist) umlaufstatus(Depot/Umlauf)",
      file=open("EventList.txt", "a"))


########################## Objekt Vehicle #########################################
def vehicle(env, vehID):  # Eigenschaften von jedem Fahrzeug
    while True:
        delayTime = 0  # DelayTime initialisieren (gilt für den ganze Tag des Fahrzeugs)

        for teilumlaufnummer in range(0, len(StartTime_dic) - 1):  # Loop der durch die einzelnen Teilumläufe führt
            try:
                yield env.timeout(
                    StartTime_dic[vehID][teilumlaufnummer] - env.now)  # Timeout bis Start des Teilumlaufes
                umlaufstatus = 1  # Wenn Startzeit erreicht, Fahrzeug im Umlauf (umlaufstatus = 1)

                while umlaufstatus == 1:  # while Fahrzeug im Umlauf
                    for fahrtnummer in range(0, len(ToHS_dic[vehID][teilumlaufnummer]) + 1):

                        # Einstellen des Störfaktors
                        delayTime_perDrive = stoerfaktor(0)
                        delayTime = delayTime + delayTime_perDrive  # Aufsummieren der Verspätungen im Teilumlauf

                        # Event: Bus fährt um bestimmte Uhrzeit von HS los
                        AbfahrtAnkunft = 0  # Abfahrt = 0, Ankunft = 1
                        print(vehID + 1, FromHS_dic[vehID][teilumlaufnummer][fahrtnummer], AbfahrtAnkunft, env.now,
                              umlaufstatus,
                              file=open("EventList.txt", "a"))

                        # Abfrage, ob Fahrt außerhalb der Simulationszeit liegen würde
                        if drive_outOfTime(DriveDuration[vehID][teilumlaufnummer][fahrtnummer], delayTime, env.now):
                            print(vehID + 1, FromHS_dic[vehID][teilumlaufnummer][fahrtnummer], AbfahrtAnkunft, env.now, 404,
                                  file=open("EventList.txt", "a"))
                            yield env.timeout(1440)
                            break

                        # Timeout für Fahrtdauer zur nächsten Haltestelle
                        yield (env.timeout(DriveDuration[vehID][teilumlaufnummer][fahrtnummer] + delayTime))

                        # Event: Bus kommt zu bestimmter Uhrzeit an HS an
                        AbfahrtAnkunft = 1
                        # Abfrage ob Bus im Depot angekommen
                        if ToHS_dic[vehID][teilumlaufnummer][fahrtnummer] == DepotID[vehID]:
                            umlaufstatus = 0
                            print(vehID + 1, DepotID[vehID], AbfahrtAnkunft, env.now, umlaufstatus,
                                  file=open("EventList.txt", "a"))
                            break
                        else:
                            print(vehID + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer], AbfahrtAnkunft, env.now,
                                  umlaufstatus,
                                  file=open("EventList.txt", "a"))

                # Counter für Drive_DurationListe übertragen
                yield env.timeout(StartTime_dic[vehID][teilumlaufnummer + 1] - env.now)

            except:
                continue

            ########################## Simulationsumgebung ##############################


env = simpy.Environment()

# Initialisierung von Fahrzeugen
for i in range(0, 1):  # Anzahl von Fahrzeugen = len(numberVeh)
    env.process(vehicle(env, i))  # Inputdaten Eigenschaften Fahrzeugen
    # Problem: BlockID fängt bei 1 an. Alle Listen und Dictionarys fangen immer bei 0 an. Mismatch gelöst mit (-1)
# Simulation starten und Laufzeit festlegen
env.run(until=1440)  # Ein Tag simulieren: in Minuten ausdrücken. 24h = 1440min
