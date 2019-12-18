#Sprint4.3

# Verspätungsframework in Loop
# Teilumläufe verknüpft


# überall kleine Fehler im Output (Daten Schuld? Datenqualität überprüfen)


# Bei Durchführung Error in den Daten ausgefallen:
#   Bei VehID 9, 77, 63 sind die Teilumläufe nicht in korrekter Reihenfolge
#   Idee: Zeiten aufsteigend sortieren bei Transformieren


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

# DepotID (jedem Fahrzeug die unique DepotID zuordnen
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

numTU_proF = []
for i in range(0,len(numberVeh)):
    numTU_proF.append(len(StartTime_dic[i])-1)
print("Die Fahrzeuge fahren im Schnitt %d Teilumläufe am Tag."
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
    
    
############################## Funktionen für Objekt Vehicle #############################

# Abfrage: Fahrtzeit über Simulationsdauer
def drive_outOfTime(time, clock):
    doOT = time + clock > 1440
    return doOT




############################ Störgenerator##################################
S = 5 # Einstellen des Störfaktors

def stoerfaktor(s):  # n = Eingabeparameter um Störausmaß zu steuern
    if (s == 0):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                              0.0])  # Wahrscheinlichkeiten von Störungen / für jeden
        # Teilfahrt neuen Störfaktor
    elif (s == 1):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.6, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                              0.0])  # Wahrscheinlichkeiten von Störungen / für jeden
        # Teilfahrt neuen Störfaktor
    elif (s == 2):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.6, 0.0, 0.0, 0.2, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0,
                                                              0.0])  # Wahrscheinlichkeiten von Störungen / für jeden
        # Teilfahrt neuen Störfaktor
    elif (s == 3):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.33, 0.0, 0.0, 0.0, 0.0, 0.33, 0.0, 0.0, 0.0, 0.0,
                                                              0.34])  # Wahrscheinlichkeiten von Störungen / für
        # jeden Teilfahrt neuen Störfaktor
    elif (s == 4):
        factorX = numpy.random.choice(numpy.arange(0, 11), p=[0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0,
                                                              0.5])  # Wahrscheinlichkeiten von Störungen / für
        # jeden Teilfahrt neuen Störfaktor
    elif (s == 5):
        factorX = 20
    return factorX

##Verspätungen außerhalb der Simulation bilden

def verspätung():

    for fzg in range(1,len(numberVeh) + 1):
        shift = 0
        for partNbr in range(0, len(StartTime_dic[fzg-1])-1):
            if partNbr > 0:                ##wenn es nicht der erste teilumlauf ist, kann es zu abhängigkeiten zw den umläufen kommen
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

                ##Für jeden Teilumlauf die einzelnen Fahrten durchiterieren
            for journey in range(0, len(PartStartTime_dic[fzg-1][partNbr])):
                if journey > 0:
                    PartStartTime_dic[fzg-1][partNbr][journey] = PartEndTime_dic[fzg-1][partNbr][journey-1]
                ##Wenn es keine Standzeit ist:
                if Journey_dic[fzg-1][partNbr][journey] != 9:
                    delaytime = stoerfaktor(2) ##Hier werden die Störfaktoren eingebaut
                    shift += delaytime
                    PartEndTime_dic[fzg-1][partNbr][journey] = PartStartTime_dic[fzg-1][partNbr][journey] + DriveDuration_dic[fzg-1][partNbr][journey] + delaytime
                ##Wenn es eine Standzeit ist:
                if Journey_dic[fzg-1][partNbr][journey] == 9:
                    ##Wenn Verschiebung größer/gleich der Pausenzeit
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
                    
verspätung()                    



def carTraffic(time):
    if var1.get() == 1:
        if (time >= 390 and time <= 510) or (time >= 1110 and time <= 1200):
            return (stoerfaktor(4))
    ##oder ggf prozentual die duration erhören? (30% mehr zu den stoßzeiten?)
        else:
            return (stoerfaktor(1))
    else:
        return(stoerfaktor(0))
    
    
def weather():
    #number = randint(1,40)
    #if number <= 4:
     #   return(stoerfaktor(5))
    #elif number <= 14:
     #   return(stoerfaktor(3))
    #else:
     #   return(stoerfaktor(1))
     if var2.get() == 1:
        return(stoerfaktor(4))
     elif var3.get() == 1:
        return(stoerfaktor(3))
     elif var4.get() == 1:
        return(stoerfaktor(1))
     else:
        return(stoerfaktor(0))
    
############################## Daten für CSV-Datei ###############################
# Header für CSV-Datei
print("vehID Teilumlaufnummer Standort Dep/Arr Uhrzeit(Soll) Uhrzeit(Ist) Fahrtverspätung Gesamtverspätung",
      file=open("Eventqueue4.3.csv", "a"))
########################## Objekt Vehicle #########################################
def vehicle(env, vehID):  # Eigenschaften von jedem Fahrzeug
    while True:
        delayTime = 0  # DelayTime initialisieren (gilt für den ganze Tag des Fahrzeugs)

        for teilumlaufnummer in range(0, len(StartTime_dic)-1):  #Loop der durch die einzelnen Teilumläufe führt
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
                            fahrtstatus = 0 # 0 = Abfahrt / 1 = Ankunft / 2 = Pause

                        delayTime_perDrive = 0 #für PrintAusgabe hier definiert
                        print(vehID + 1, teilumlaufnummer + 1, FromHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                              fahrtstatus, PartStartTime_dic[vehID][teilumlaufnummer][fahrtnummer], env.now,
                              "-", delayTime,
                              file=open("Eventqueue4.3.csv", "a"))

                        # Verspätung auf Fahrt ermitteln
                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            delayTime_perDrive = 0
                        else:
                            delayTime_perDrive = carTraffic(env.now) + weather()

                        # Aufsummieren der Verspätungen im Teilumlauf
                        delayTime += delayTime_perDrive

                        # Abfrage, ob Fahrt außerhalb der Simulationszeit liegen würde
                        if drive_outOfTime(
                                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer], env.now):
                            yield env.timeout(1440)
                            break

                        # Abfrage, ob Pausenzeit
                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] = \
                                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] - delayTime
                            if DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] < 0:
                                delayTime = abs(DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer])
                                DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] = 0
                            else:
                                delayTime = 0


                        # Timeout für Fahrtdauer zur nächsten Haltestelle
                        yield (env.timeout(DriveDuration_dic[vehID][teilumlaufnummer][fahrtnummer] + delayTime_perDrive))

                        if ElementID_dic[vehID][teilumlaufnummer][fahrtnummer] == 9:
                            fahrtstatus = 2
                        else:
                            fahrtstatus = 1

                        # Abfrage ob Bus im Depot angekommen
                        if ToHS_dic[vehID][teilumlaufnummer][fahrtnummer] == DepotID[vehID]:
                            print(vehID + 1, teilumlaufnummer + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  fahrtstatus, PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  env.now, delayTime_perDrive, delayTime,
                                  file=open("Eventqueue4.3.csv", "a"))
                            umlaufstatus = 0
                        else:
                            print(vehID + 1, teilumlaufnummer + 1, ToHS_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  fahrtstatus, PartEndTime_dic[vehID][teilumlaufnummer][fahrtnummer],
                                  env.now, delayTime_perDrive, delayTime,
                                  file=open("Eventqueue4.3.csv", "a"))

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
env.run(until=1440)  # Ein Tag simulieren: in Minuten ausdrücken. 24h = 1440min