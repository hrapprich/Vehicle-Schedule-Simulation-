#Sprint1

#Import Packages
import simpy
import pandas as pd

#Daten einlesen & charakterisieren
df = pd.read_csv("/home/chris/PythonProjekte/SemProjekt-1920/SimPy/tableFinal.csv", sep=";")
#df.info()


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
    if (counter == i):
        x = df.DepotID[i]
        DepotID.append(x)
    counter += 1
print("Jedes Fahrzeug besitzt eine DepotID: %s" %(len(DepotID) == len(numberVeh))) #Frage: Hat jedes Fahrzeug nur ein Depot oder kann das wechseln??

###VehStatus / im Depot(0), im Umlauf (1)
VehStatus = 0 #Alle Fahrzeuge stehen am Anfang im Depot

###StartTime (Dictionary mit allen Startzeiten der Teilumläufe des entsprechenden Fahrzeugs)
''' Schleife funktioniert noch nicht
startTime_dic = {}
counter = 0
for i in range(1, len(numberVeh)):
    for j in range(len(df)):
        if(df.BlockID[j] == i):
            if(df.FromStopID[j] == DepotID[i]):
                print(df.DepTime[j])
                counter +=1
                #startTime_dic.update({i: df.DepTime[j]})

counter #müssen mindestens 100 sein
startTime_dic
'''
#Behilfswerte
startTime_dic = {   0: [251, 600, 1440], 
                    1: [260, 1020, 1440]} #Startzeiten in Minuten umrechnen (von 0 hoch) / 4h 11min = 60*4 + 11 = 251 Timesteps // 1440 am Ende, damit Loop in def vehicle nicht out of range is
StartTime = startTime_dic

###Listen von Haltestellen (from/to): automatisieren (offen)
Veh1_fromStop = list(range(1,11))
Veh2_fromStop = list(range(50,61))
FromStopID = [Veh1_fromStop,Veh2_fromStop]


Veh1_toStop = list(range(11,20)) + [DepotID[0]]
Veh2_toStop = list(range(61,70)) + [DepotID[1]]
ToStopID = [Veh1_toStop, Veh2_toStop]

#Fahrzeit zwischen den einzelnen Stationen: automatisieren (offen)
Veh1_drive_duration = [5,5,5,5,5,5,5,5,5,5]
Veh2_drive_duration = [10,5,10,5,10,5,10,5,10,5]
DriveDuration = [Veh1_drive_duration, Veh2_drive_duration]

#########Notizen#############
#Teilumläufe erstmal auf = 1 reduzieren

#Prozesse und Events von Objekt Vehicle
def vehicle(env, name, vehID, vehStatus, depotID, startTime, fromStopID, toStopID, driveDuration):#Eigenschaften von jedem Fahrzeug
    while True:
        print("%s. VehID %d. VehStatus %d. DepotID: %d. StartTime: %d. FromStopID: %d. ToStopID: %d. DriveDuration: %d. Clock: %f " % (name, vehID, vehStatus, depotID, startTime, fromStopID, toStopID, driveDuration, env.now))
        for j in range(0,2): #Anzahl Teilumläufe des Fahrzeugs
            time_untilStart = StartTime[vehID][j] - env.now #Startzeit des jeweiligen Umlaufs
            yield env.timeout(time_untilStart) #Timeout bis Start des Umlaufes
            status = 1 #Wenn Startzeit erreicht, Fahrzeug im Umlauf
            print("%s. Status %d. Clock: %f" %(name, status, env.now))
            while (status == 1):
                for k in range(len(ToStopID[vehID])):
                    print("%s drives from %d to %d. Clock: %f" %(name, FromStopID[vehID][k], ToStopID[vehID][k], env.now))
                    yield env.timeout(DriveDuration[vehID][k])
                    if (ToStopID[vehID][k] == DepotID[vehID]):
                        status = 0   
            print("Drive ends here, Vehicle %d back in Depot %d. Clock: %f"%(vehID, DepotID[vehID], env.now))
            yield env.timeout(StartTime[vehID][j+1]-env.now)
        yield env.timeout(1000)
        print("End of the Day. Every Vehicle is back in Depot")

        
#Simulationsumgebung initialisieren      
env = simpy.Environment()

#Initialisierung von Fahrzeugen
for i in range(0,2):#Anzahl von Fahrzeugen
    env.process(vehicle(env, "Vehicle:%d"%i , i, VehStatus, DepotID[i], StartTime[i][0], FromStopID[i][0], ToStopID[i][0], DriveDuration[i][0]))#Inputdaten Eigenschaften Fahrzeugen

#Simulation starten und Laufzeit festlegen
env.run(until = 1440) #Ein Tag simulieren: in Minuten ausdrücken. 24h = 1440min 


#The run process is automatically started when Car is instantiated (S.6)
# -> für uns weniger Sinn, weil Fahrzeuge stehen zuerst alle im Depot, also werden alle gleichzeitig initialisiert