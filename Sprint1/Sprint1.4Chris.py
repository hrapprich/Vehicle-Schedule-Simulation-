#Sprint1
#Änderungen zu 1.3:

#Störung eingebaut und Teilumläufe verknüpft (simple Abhängigkeit, noch ausbaufähig ;) )
#Print-Ausgaben werden automatisch in Text-File geschrieben (TrackingList)
#-Daten nicht per Print-Befehl ausgeben lassen, sondern in .csv abspeichern (Umweg über .txt)

#ToDos:

# - Komplexere Abhängigkeiten
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

df.StartTime[9]
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
    startTime_dic.update({(i): startTimes_Block})

StartTime_dic = startTime_dic
StartTime_dic

StartTime_dic[45]

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

DriveDuration[0]
ToStopID[0]
#################Test########################

#####################################################

#Störungen generieren: factorX
import numpy

def stoerfaktor(n):
    if (n==0):
        factorX = numpy.random.choice(numpy.arange(0,11), p=[1.0, 0.0, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]) #Wahrscheinlichkeiten von Störungen / für jeden Teilfahrt neuen Störfaktor
    elif (n==1):
        factorX = numpy.random.choice(numpy.arange(0,11), p=[0.6, 0.0, 0.0,0.0,0.0,0.2,0.0,0.0,0.0,0.0,0.2]) #Wahrscheinlichkeiten von Störungen / für jeden Teilfahrt neuen Störfaktor
    elif (n==2):
        factorX = numpy.random.choice(numpy.arange(0,11), p=[0.33, 0.0, 0.0,0.0,0.0,0.33,0.0,0.0,0.0,0.0,0.34]) #Wahrscheinlichkeiten von Störungen / für jeden Teilfahrt neuen Störfaktor
    return factorX

#Daten für CSV-Dateo
print("vehID FromStopID ToStopID Uhrzeit(Ist) Uhrzeit(Soll) Delay Drive_Continue", file = open("DelayCSV.txt", "a")) #Daten für CSVFile

#Prozesse und Events von Objekt Vehicle
def vehicle(env, name, vehID, vehStatus, depotID, startTime, fromStopID, toStopID, driveDuration):#Eigenschaften von jedem Fahrzeug
    while True:
        print("%s. VehID %d. VehStatus %d. DepotID: %d. StartTime: %d." % (name, vehID, vehStatus, depotID, startTime), file = open("TrackingList.txt", "a"))
        counter = 0
        delayTime = 0 #DelayTime initialisieren (gilt für den ganze Tag des Fahrzeugs)
        
        
        for j in range(0,len(StartTime_dic)-1): #Anzahl Teilumläufe des Fahrzeugs
           
            time_untilStart = StartTime_dic[vehID][j] - env.now #Startzeit des jeweiligen Umlaufs
            yield env.timeout(time_untilStart) #Timeout bis Start des Umlaufes
            status = 1 #Wenn Startzeit erreicht, Fahrzeug im Umlauf
            print("%s. Status %d. Clock: %f" %(name, status, env.now), file = open("TrackingList.txt", "a"))
            
            
            while (status == 1):
                cache_counter = 0 #wichtig, weil Start und EndHaltestellen in einer Liste, sodass counter TeilumlaufHaltestellen abgrenzt
                for k in range(0,len(ToStopID[vehID-1])):
                    
                    #Einstellen des Störfaktors
                    delayTime_perDrive = stoerfaktor(1) 
                    delayTime = delayTime + delayTime_perDrive #Aufsummieren der Verspätungen im Teilumlauf

                    if (ToStopID[vehID-1][k+counter] == DepotID[vehID-1]):
                        cache_counter += 1
                        status = 0 
                        #Daten für CSV
                        drive_continue = "no"
                        print(vehID, FromStopID[vehID-1][k+counter], ToStopID[vehID-1][k+counter], env.now, env.now-delayTime, (env.now - (env.now-delayTime)), drive_continue, file = open("DelayCSV.txt", "a"))
                        break
                    else: 
                        print("%s drives from %d to %d. Delay: %d. Clock: %f." %(name, FromStopID[vehID-1][k+counter], ToStopID[vehID-1][k+counter], delayTime, env.now), file = open("TrackingList.txt", "a"))
                        
                        #Daten für CSV-Output
                        drive_continue = "yes"
                        print(vehID, FromStopID[vehID-1][k+counter], ToStopID[vehID-1][k+counter], env.now, env.now-delayTime, (env.now - (env.now-delayTime)) ,drive_continue, file = open("DelayCSV.txt", "a")) 
                        
                        cache_counter += 1
                        if (DriveDuration[vehID-1][k+counter] + delayTime + env.now >= 1440):
                            print("ENDE IM GELÄNDE. Wenn %s noch nicht im Depot ist, dann fährt es noch heute..." %(name), file = open("TrackingList.txt", "a"))
                            print(vehID, 404, 404, 404, 404, 404, 404, file = open("DelayCSV.txt", "a"))
                            yield env.timeout(DriveDuration[vehID-1][k+counter] + delayTime)   
                        else:  
                            yield env.timeout(DriveDuration[vehID-1][k+counter] + delayTime)
                    

            print("Drive ends here, Vehicle %d comes back from Drive Nr.%d from Stop %d in Depot %d. Clock: %f"%(vehID, j+1, FromStopID[vehID-1][k+counter],  DepotID[vehID-1], env.now), file = open("TrackingList.txt", "a"))
            counter = counter + cache_counter
            #Abfrage ob AnschlussUmlauf erreicht wird
            if (StartTime_dic[vehID][j+1]-env.now < 0):
                print("GAME OVER. Vehicle %d does not reach next StartTime. Every drive afterwards is cancelled #BVG" %vehID, file = open("TrackingList.txt", "a"))
                yield env.timeout(1440)
            else:
                yield env.timeout(abs(StartTime_dic[vehID][j+1]-env.now))
                delayTime = 0 #gesammelten Verspätungen hatten keinen Impact auf weiterführende Teilumläufe (RESET)
        
        print("End of the Day. Every Vehicle is back in Depot") #useless
        yield env.timeout(100000) #useless
        

        
#Simulationsumgebung initialisieren      
env = simpy.Environment()

#Initialisierung von Fahrzeugen
for i in range(1, len(numberVeh)+1):#Anzahl von Fahrzeugen = len(numberVeh)+1
    env.process(vehicle(env, "Vehicle:%d"%i , i, VehStatus, DepotID[i-1], StartTime_dic[i][0], FromStopID[i-1][0], ToStopID[i-1][0], DriveDuration[i-1][0]))#Inputdaten Eigenschaften Fahrzeugen
#Problem: BlockID fängt bei 1 an. Alle Listen und Dictionarys fangen immer bei 0 an. Mismatch

#Simulation starten und Laufzeit festlegen
env.run(until = 1440) #Ein Tag simulieren: in Minuten ausdrücken. 24h = 1440min 

#Wenn Simulation mit 100 Fahrzeugen Print-Ausgaben abstellen -> Daten in .csv extrahieren für Asuwertung

