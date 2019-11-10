#Sprint1

#ToDos:
# - StartTimes der Teilumläufe jedes Fahrzeugs in Dictionary abspeichern
# - Haltestellen (From/To) extrahieren (in welcher Form macht das Sinn (auch Dic?))
# - Fahrtzeiten zwischen den Haltestellen errechen (Arr-Dep) und abspeichern

# - kleine Störung einbauen (bei timeout macht wahrscheinlich am meisten Sinn)
# - Abhängigkeiten zwischen den Teilumläufen schaffen

# - Überlegen wie man clever die Fahrer (DutyID) einbaut

#Import Packages
import simpy
import pandas as pd

#Daten einlesen & charakterisieren
df = pd.read_csv("/home/chris/PythonProjekte/SemProjekt-1920/SimPy/tableFinal.csv", sep=";")
#df.info()

#Daten transformieren (Zeit)
StartTime = []
count_row = df.shape[0]
for x in range(0, count_row):
    min_time = df.iloc[x,5].split(":")
    minutes = int(min_time[1]) * 60
    minutes = minutes + int(min_time[2])
    StartTime.append(minutes)

EndTime = []
count_row = df.shape[0]
for x in range(0, count_row):
    min_time = df.iloc[x,6].split(":")
    minutes = int(min_time[1]) * 60
    minutes = minutes + int(min_time[2])
    EndTime.append(minutes)

df["EndTime"] = EndTime
df["StartTime"] = StartTime

df.StartTime[0]
df.EndTime[0]




###Werkstatt für Ausprägungen /#Ausprägungen der Eigenschaftenn bei Initialisierung

###Number of Vehicles
numberVeh = df["BlockID"].unique()
numberVeh = numberVeh.tolist() #von Array in Liste formatieren
numberVeh = [elem for elem in numberVeh if elem >= 0] #-1 entfernen
print("Die Gesamtanzahl von Fahrzeugen beträgt %d." %len(numberVeh))

###DepotID
DepotID = []
counter = 1
for i in range(1, len(numberVeh)+1):
    for j in range(0,df.shape[0]):
        if(df.BlockID[j] == i and counter == i):
            DepotID.append(df.DepotID[j])
            counter += 1
            
print("Jedes Fahrzeug besitzt eine DepotID: %s" %(len(DepotID) == len(numberVeh))) #Frage: Hat jedes Fahrzeug nur ein Depot oder kann das wechseln??

###VehStatus / im Depot(0), im Umlauf (1)
VehStatus = 0 #Alle Fahrzeuge stehen am Anfang im Depot

###StartTime (Dictionary mit allen Startzeiten der Teilumläufe des entsprechenden Fahrzeugs)

DepotID_plusOne = [0] + DepotID #DepotIDListe verlängern, damit Schleife mit i funktioniert
startTime_dic = {}
for i in range(1, len(numberVeh)+1):
    startTimes_Block = []
    for j in range(len(df)):
        if(df.BlockID[j] == i):
            if(df.FromStopID[j] == DepotID_plusOne[i]):
                startTimes_Block.append(df.StartTime[j])
    startTimes_Block = startTimes_Block + [1440] #Add to every list a 1440 as last element for simulation loop (timeout)
    startTime_dic.update({(i-1): startTimes_Block})

StartTime_dic = startTime_dic
StartTime_dic

print("Jedes Fahrzeug fährt mindestens einmal aus dem Depot: %s" %(len(StartTime_dic) == len(numberVeh)))

'''
#Behilfswerte
startTime_dic = {   0: [251, 600, 1440], 
                    1: [260, 1020, 1440]} #Startzeiten in Minuten umrechnen (von 0 hoch) / 4h 11min = 60*4 + 11 = 251 Timesteps // 1440 am Ende, damit Loop in def vehicle nicht out of range is
StartTime = startTime_dic
len(StartTime)
'''

###Listen von Haltestellen (from/to): automatisieren (ready)
'''
Veh1_fromStop = list(range(1,11))
Veh2_fromStop = list(range(50,61))
FromStopID = [Veh1_fromStop,Veh2_fromStop]

Veh1_toStop = list(range(11,20)) + [DepotID[0]]
Veh2_toStop = list(range(61,70)) + [DepotID[1]]
ToStopID = [Veh1_toStop, Veh2_toStop]
'''

FromStopID = []
ToStopID = []
for i in range(1, len(numberVeh)+1):
    fromStopID_cache = []
    toStopID_cache = []
    for j in range(0, df.shape[0]):
        if(df.BlockID[j] == i):
            fromStopID_one = df.iloc[j,3]
            fromStopID_cache.append(fromStopID_one)
            toStopID_one = df.iloc[j,4]
            toStopID_cache.append(toStopID_one)
    FromStopID.append(fromStopID_cache)
    ToStopID.append(toStopID_cache)
print("Die Anzahl der StoppointListen (from) ist gleich der Anzahl der Fahrzeuge: %s."%(len(FromStopID) == len(numberVeh)))
print("Die Anzahl der StoppointListen (to) ist gleich der Anzahl der Fahrzeuge: %s."%(len(ToStopID) == len(numberVeh)))

#Fahrzeit zwischen den einzelnen Stationen: automatisieren (ready)
'''
Veh1_drive_duration = [5,5,5,5,5,5,5,5,5,5]
Veh2_drive_duration = [10,5,10,5,10,5,10,5,10,5]
DriveDuration = [Veh1_drive_duration, Veh2_drive_duration]
'''


DriveDuration = []
for i in range(1, len(numberVeh)+1):
    DifTime = []
    for j in range(0, df.shape[0]):
        if(df.BlockID[j] == i):
            difTime = df.iloc[j,12] - df.iloc[j,13]
            DifTime.append(difTime)
    DriveDuration.append(DifTime)
print("Die Anzahl der Fahrtzeitlisten ist gleich der Anzahl der Fahrzeuge: %s."%(len(DriveDuration) == len(numberVeh)))

#################Test########################

#####################################################

#Störungen generieren: factorX
#import numpy
#factorX = numpy.random.choice(numpy.arange(0,5), p=[0.4, 0.1, 0.05, 0.05, 0.4]) #Wahrscheinlichkeiten von Störungen

#Prozesse und Events von Objekt Vehicle
def vehicle(env, name, vehID, vehStatus, depotID, startTime, fromStopID, toStopID, driveDuration):#Eigenschaften von jedem Fahrzeug
    while True:
        print("%s. VehID %d. VehStatus %d. DepotID: %d. StartTime: %d. FromStopID: %d. ToStopID: %d. DriveDuration: %d. Clock: %f " % (name, vehID, vehStatus, depotID, startTime, fromStopID, toStopID, driveDuration, env.now))
        for j in range(0,len(StartTime_dic)-1): #Anzahl Teilumläufe des Fahrzeugs
            time_untilStart = StartTime_dic[vehID-1][j] - env.now #Startzeit des jeweiligen Umlaufs
            yield env.timeout(time_untilStart) #Timeout bis Start des Umlaufes
            status = 1 #Wenn Startzeit erreicht, Fahrzeug im Umlauf
            print("%s. Status %d. Clock: %f" %(name, status, env.now))
            while (status == 1):
                for k in range(len(ToStopID[vehID-1])):
                    print("%s drives from %d to %d. Clock: %f." %(name, FromStopID[vehID-1][k], ToStopID[vehID-1][k], env.now))
                    yield env.timeout(DriveDuration[vehID-1][k])
                    if (ToStopID[vehID-1][k] == DepotID[vehID-1]):
                        status = 0   
            print("Drive ends here, Vehicle %d back from Drive Nr.%d in Depot %d. Clock: %f"%(vehID, j+1, DepotID[vehID-1], env.now))
            yield env.timeout(StartTime_dic[vehID-1][j+1]-env.now)
        yield env.timeout(100000)
        print("End of the Day. Every Vehicle is back in Depot")

        
#Simulationsumgebung initialisieren      
env = simpy.Environment()

#Initialisierung von Fahrzeugen
for i in range(1,len(numberVeh)+1):#Anzahl von Fahrzeugen
    env.process(vehicle(env, "Vehicle:%d"%i , i, VehStatus, DepotID[i-1], StartTime_dic[i-1][0], FromStopID[i-1][0], ToStopID[i-1][0], DriveDuration[i-1][0]))#Inputdaten Eigenschaften Fahrzeugen
#Problem: BlockID fängt bei 1 an. Alle Listen und Dictionarys fangen immer bei 0 an. Mismatch

#Simulation starten und Laufzeit festlegen
env.run(until = 1440) #Ein Tag simulieren: in Minuten ausdrücken. 24h = 1440min 

#Wenn Simulation mit 100 Fahrzeugen Print-Ausgaben abstellen -> Daten in .csv extrahieren für Asuwertung

#The run process is automatically started when Car is instantiated (S.6)
# -> für uns weniger Sinn, weil Fahrzeuge stehen zuerst alle im Depot, also werden alle gleichzeitig initialisiert