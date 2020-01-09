####################### Import Packages ###################################
import simpy
import pandas as pd
import numpy
from random import randint
from tkinter import *


root = Tk()
root.geometry("300x200")
var1 = IntVar()
c1 = Checkbutton(root, text='An diesem Tag gibt es Berufsverkehr.', variable=var1)
var2 = IntVar()
c2 = Checkbutton(root, text='An diesem Tag gibt es Gewitter.', variable=var2)
var3 = IntVar()
c3 = Checkbutton(root, text='An diesem Tag regnet es.', variable=var3)
var4 = IntVar()
c4 = Checkbutton(root, text='An diesem Tag scheint die Sonne.', variable=var4)
button = Button(text = "Bestätigen", bg = "green", command = root.destroy)

c1.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
c2.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
c3.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
c4.pack(side='top', fill='x', padx='5', pady='5', anchor = "w")
button.pack(side='bottom', fill='y', padx='5',pady='10')

mainloop()

####################### Daten einlesen ####################################
df = pd.read_csv("/home/chris/PythonProjekte/SemProjekt-1920/tableFinal.txt", sep=";")
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
print("Es gibt %d verschiedene Depots." % (len(set(DepotID))))
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
        {(
                     i - 1): startTimes_Block})  # i-1 damit Index bei 0 anfÃ¤ngt (wichtig fÃ¼r Schleife (nachtrÃ¤gliche Ãnderung!)

StartTime_dic = startTime_dic

numTU_proF = []
for i in range(0, len(numberVeh)):
    numTU_proF.append(len(StartTime_dic[i]) - 1)
print("Die Fahrzeuge fahren im Schnitt %d TeilumlÃ¤ufe am Tag."
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

##fÃ¼r die Annahme, dass ein Stau eher im Zentrum ist (Annahme, dass Zentrum dort ist, wo eine Haltestelle stark befahren wird)
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


############################## Funktionen fÃ¼r Objekt Vehicle #############################

# Abfrage: Fahrtzeit Ã¼ber Simulationsdauer
def drive_outOfTime(time, clock):
    doOT = time + clock > 1440
    return doOT


############################ Störgenerator##################################

def globalDisruption(driveduration):
    if var2.get() == 1: #Gewitter
        ausmaß = 0.8 # Anteil an Fahrten, die von Störung betroffen sind
        delayonTop = 0.6 # Verspätung, die abhängig von Fahrtzeit on Top auf die Fahrtzeit raufkommt
    elif var3.get() == 1: #Regen
        ausmaß = 0.5
        delayonTop = 0.4
    elif var4.get() == 1: #Sonne
        ausmaß = 0.2
        delayonTop = 0.2
    else:
        ausmaß = 0
        delayonTop = 0
    coin = numpy.random.choice(numpy.arange(0, 2), p=[1-ausmaß, ausmaß])
    if (coin==1):
        delay = int(driveduration*delayonTop)
    else:
        delay = 0
    return delay #Type der Störung bei Ausgabe angeben (durch Input Checkbox bestimmt)(Funktion immer dieselbe)

def selectionDisruption(fromhs, tohs, driveduration, time):
    if varInnenstadtStau.get() == 1:
        if fromhs in Innenstadthaltestellen or tohs in Innenstadthaltestellen:
            ausmaß = 1
            delayonTop = 0.4
            if (time >= 390 and time <= 510) or (time >= 1110 and time <= 1200):
                delayonTop = 0.8
    elif FromHS in Jam or ToHS in Jam:
        ausmaß = 1
        delayonTop = 0.4
    else:
        ausmaß = 0
        delayonTop = 0
    coin = numpy.random.choice(numpy.arange(0, 2), p=[1 - ausmaß, ausmaß])
    if (coin == 1):
        delay = int(driveduration * delayonTop)
    else:
        delay = 0
    return delay  # Type der Störung bei Ausgabe angeben (durch Input Checkbox bestimmt)(Funktion immer dieselbe)


def breaktime(vehID, teilumlaufnummer, fahrtnummer, delayTime):
    if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
        DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] = \
            DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] - delayTime
        if DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] < 0:
            delayTime = abs(DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer])
            DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] = 0
        else:
            delayTime = 0
    return (delayTime)


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
    return (delayType)


############################## Daten fÃ¼r CSV-Datei ###############################
# Header fÃ¼r CSV-Datei
print(
    "vehID Teilumlaufnummer Standort Dep/Arr Uhrzeit(Soll) Uhrzeit(Ist) FahrtverspÃ¤tung GesamtverspÃ¤tung VerspÃ¤tungsursache",
    file=open("eventqueue5.2.csv", "a"))


########################## Objekt Vehicle #########################################
def vehicle(env, vehID):  # Eigenschaften von jedem Fahrzeug
    while True:
        delayTime = 0  # DelayTime initialisieren (gilt fÃ¼r den ganze Tag des Fahrzeugs)
        delayType = ""
        for teilumlaufnummer in range(0, len(StartTime_dic) - 1):  # Loop der durch die einzelnen TeilumlÃ¤ufe fÃ¼hrt
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
                            fahrtstatus = 0  # 0 = Abfahrt / 1 = Ankunft / 2 = Pause

                        delayTime_perDrive = 0  # fÃ¼r PrintAusgabe hier definiert
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
                            delayGlobal = globalDisruption(DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer])
                            delaySelection = selectionDisruption(FromHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                                                 ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                                                 DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer],
                                                                 env.now)
                            #delaySpecific = specificDisruption()
                            delayTime_perDrive = delayGlobal + delaySelection

                            # FÃ¼ge der Outputvariable "delayType" den Grund der VerspÃ¤tung hinzu
                            #delayType = Type(delayWeather, delayCarTraffic, delayTrafficJam)

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
                                  file=open("eventqueue5.2.csv", "a"))
                            umlaufstatus = 0
                        else:
                            print(vehID + 1, teilumlaufnummer + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  fahrtstatus, PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  env.now, delayTime_perDrive, delayTime, delayType,
                                  file=open("eventqueue5.2.csv", "a"))

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
env.run(until=1440)  # Ein Tag simulieren: in Minuten ausdrÃ¼cken. 24h = 1440min
