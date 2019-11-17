# Sprint2.1
# Neuerungen:
# - Eventliste auf Fahrtebene (Eintrag wenn Bus abfährt & wenn Bus ankommt)
# - Versuch einer dispositiven Abhängigkeit

# ToDos:
# - Komplexere Abhängigkeiten
# - Fahrer (DutyID) einbauen
# - Dispositives System schaffen (als LongTermGoal)

####################### Import Packages ###################################
import simpy
import pandas as pd
import numpy

####################### Daten einlesen ####################################
df = pd.read_csv("/home/chris/PythonProjekte/SemProjekt-1920/SimPy/tableFinal.csv", sep=";")
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
    startTime_dic.update({(i): startTimes_Block})

StartTime_dic = startTime_dic
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


############################## Funktionen für Objekt Vehicle ##############################

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
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.6, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0,
                                                              0.2])  # Wahrscheinlichkeiten von Störungen / für jeden
        # Teilfahrt neuen Störfaktor
    elif (n == 2):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.33, 0.0, 0.0, 0.0, 0.0, 0.33, 0.0, 0.0, 0.0, 0.0,
                                                              0.34])  # Wahrscheinlichkeiten von Störungen / für
        # jeden Teilfahrt neuen Störfaktor
    return factorX


############################## Daten für CSV-Datei ###############################
# Header für CSV-Datei
print("vehID Standort Dep/Arr Uhrzeit(Ist) Status(Depot/Umlauf)",
      file=open("TestDelayCSV.txt", "a"))


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
                for k in range(0, len(ToStopID[vehID - 1])):

                    # Einstellen des Störfaktors
                    delayTime_perDrive = stoerfaktor(1)
                    delayTime = delayTime + delayTime_perDrive  # Aufsummieren der Verspätungen im Teilumlauf

                    # Event: Bus fährt um bestimmte Uhrzeit von HS los
                    itemDrive = 0  # Abfahrt = 0, Ankunft = 1
                    print(vehID, FromStopID[vehID - 1][k + counter], itemDrive, env.now, status,
                          file=open("TestDelayCSV.txt", "a"))

                    # Abfrage, ob Fahrt außerhalb der Simulationszeit liegen würde
                    if drive_outOfTime(DriveDuration[vehID - 1][k + counter], delayTime, env.now):
                        print(vehID, FromStopID[vehID - 1][k + counter], itemDrive, env.now, 404,
                              file=open("TestDelayCSV.txt", "a"))
                        yield env.timeout(1440)
                        break

                    # Abfrage, ob Fahrt ausgeführt werden soll, wenn AnschlussTeilumlauf dadurch nicht mehr erreicht
                    # werden kann
                    # Fehler: fährt nachm Break nicht vom Depot los
                    if (DriveDuration[vehID - 1][k + counter] + delayTime + env.now) > StartTime_dic[vehID][j + 1] \
                            and askoneTime == 0:
                        print("Soll die Fahrt abgebrochen und der nächste Teilumlauf gestartet werden?")
                        int_user = int(input("1 for continue the Drive. 2 for skip the drive: "))
                        if int_user == 1:
                            askoneTime = 1
                        else:
                            print(vehID, FromStopID[vehID - 1][k + counter], 707, env.now, 707,
                                  file=open("TestDelayCSV.txt", "a"))
                            status = 0
                            break  # Ausnahmen/Errors abfangen (offen)

                    # Timeout für Fahrtdauer zur nächsten Haltestelle
                    yield (env.timeout(DriveDuration[vehID - 1][k + counter] + delayTime))

                    # Event: Bus kommt zu bestimmter Uhrzeit an HS an
                    itemDrive = 1
                    # Abfrage ob Bus im Depot angekommen
                    if ToStopID[vehID - 1][k + counter] == DepotID[vehID - 1]:
                        status = 0
                        cache_counter += 1
                        print(vehID, DepotID[vehID - 1], itemDrive, env.now, status,
                              file=open("TestDelayCSV.txt", "a"))
                        break
                    else:
                        print(vehID, ToStopID[vehID - 1][k + counter], itemDrive, env.now, status,
                              file=open("TestDelayCSV.txt", "a"))
                        cache_counter += 1

                    # Event: wenn StartTime des nächsten Umlaufes jetzt beginnt, lieber diesen Teilumlauf abbrechen
                    # und nächsten Teilumlauf starten?

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
for i in range(1, 2):  # Anzahl von Fahrzeugen = len(numberVeh)+1
    env.process(vehicle(env, i))  # Inputdaten Eigenschaften Fahrzeugen
    # Problem: BlockID fängt bei 1 an. Alle Listen und Dictionarys fangen immer bei 0 an. Mismatch gelöst mit (-1)
# Simulation starten und Laufzeit festlegen
env.run(until=1440)  # Ein Tag simulieren: in Minuten ausdrücken. 24h = 1440min
