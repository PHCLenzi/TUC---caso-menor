from AAPI import *
import sys
import aimsunInterface.aimsun_interface as aimsun_interface
import time
from datetime import datetime
import sqlite3




# import sample_data_loader_small_arterial as loader
import sample_data_loader_small_arterial_bd as loader

db_output_replication_path = "C:\\Users\\Pedro Henrique Lenzi\\Desktop\\ECA - 20.1\\Estágio\\simulacao controle tuc caso menor\\OurputReplication.db"
# (original felipe)ld = loader.Loader("C:\\Users\\felipe\Downloads\\small_arterial.sqlite")
ld = loader.Loader("C:\\Users\\Pedro Henrique Lenzi\\Desktop\\ECA - 20.1\\Estágio\\simulacao controle tuc caso menor\\small_arterial.sqlite")
db_parameters_path = "C:\\Users\\Pedro Henrique Lenzi\\Desktop\\ECA - 20.1\\Estágio\\simulacao controle tuc caso menor\\small_arterial.sqlite"
historic_db_path = "C:\\Users\\Pedro Henrique Lenzi\\Desktop\\ECA - 20.1\\Estágio\\simulacao controle tuc caso menor\\HistoricReplicationdb.db"

aimsun_junction_to_tuc = ld.get_junction_aimsun_map(1)
aimsun_link_to_tuc = ld.get_link_aimsun_map(1)
aimsun_detector_map = ld.get_aimsun_detector_map(1)

interface = aimsun_interface.AimsunInterface(aimsun_junction_to_tuc,aimsun_link_to_tuc,aimsun_detector_map,
                                             "C:\\Users\\Pedro Henrique Lenzi\\Desktop\\ECA - 20.1\\Estágio\\simulacao controle tuc caso menor\\temp\\", loop_detector=False)

loaded = {'l': 0}

speedAverageSimulation = 0
delayAverageSimulation = 0
TDistanceAverageSimulation = 0
TTimeAverageSimulation = 0



def AAPILoad():
    #global loaded
    AKIPrintString("AAPILoad")
    AKIPrintString(str(sys.version))
    #loaded = {'l': False}
    return 0


def AAPIInit():
    
    AKIPrintString("AAPIInit")
    interface.dump_turns()
    
    #interface.disable_events()
    return 0


def AAPIManage(time, timeSta, timeTrans, acycle):
    # AKIPrintString( "AAPIManage" )
    #AKIPrintString(str(loaded['l']))
    if loaded['l'] == 0:
        interface.initialize()
        loaded['l'] = 1
    interface.initialize()
    interface.update(time, timeSta, timeTrans, acycle)
    return 0


def AAPIPostManage(time, timeSta, timeTrans, acycle):
    # AKIPrintString( "AAPIPostManage" )
    return 0




def AAPIUnLoad():
    AKIPrintString("AAPIUnLoad")
    return 0


def AAPIPreRouteChoiceCalculation(time, timeSta):
    AKIPrintString("AAPIPreRouteChoiceCalculation")
    return 0


def AAPIEnterVehicle(idveh, idsection):
    return 0


def AAPIExitVehicle(idveh, idsection):
    return 0


def AAPIEnterPedestrian(idPedestrian, originCentroid):
    return 0


def AAPIExitPedestrian(idPedestrian, destinationCentroid):
    return 0


def AAPIEnterVehicleSection(idveh, idsection, atime):
    return 0


def AAPIExitVehicleSection(idveh, idsection, atime):
    return 0

def AAPIFinish():
    #(original felipe)interface.dump_results()
    #(original felipe)AKIPrintString("AAPIFinish")
    #(original felipe)return 0
    estad = AKIEstGetGlobalStatisticsSystem(0)

    if (estad.report==0):

        AKIPrintString("\t\t SYSTEM\n")

        astring = "\t\t Report : " + str(estad.report)

        AKIPrintString(astring)

        astring = "\t\t Flow : " + str(estad.Flow)

        AKIPrintString(astring)

        astring = "\t\t Travel Time : " + str(estad.TTa)

        AKIPrintString(astring)

        astring = "\t\t Delay Time : " + str(estad.DTa)
        delayAverageSimulation = float(str(estad.DTa))
    
   
        astring = "\t\t Total Distance : " + str(estad.TotalTravel)
        AKIPrintString(astring)
        TDistanceAverageSimulation = float(str(estad.TotalTravel))

        astring = "\t\t Total Time : " + str(estad.TotalTravelTime)
        AKIPrintString(astring)
        TTimeAverageSimulation = float(str(estad.TotalTravelTime))

        astring = "\t\t Speed : " + str(estad.Sa) 
        speedAverageSimulation = float(str(estad.Sa))
        AKIPrintString(astring);

        update_avarege_Speed_db(db_output_replication_path,speedAverageSimulation)


        update_historic_db(historic_db_path,speedAverageSimulation,delayAverageSimulation,TDistanceAverageSimulation,TTimeAverageSimulation,read_from_db_parameters_path(db_parameters_path))
     

        astring = "\t\t Stop Time : " + str(estad.STa)

        AKIPrintString(astring);

        astring = "\t\t NumStops : " + str(estad.NumStops)

        AKIPrintString(astring)
        AKIPrintString("AAPIFinish")



    estad2 = AKIEstGetGlobalStatisticsSection(1, 0)

    if (estad2.report==0):

        AKIPrintString("\t\t SECTION\n")

        astring = "\t\t Report : " + str(estad2.report)

        AKIPrintString(astring)

        astring = "\t\t Flow : " + str(estad2.Flow)

        AKIPrintString(astring)

        astring = "\t\t Travel Time : " + str(estad2.TTa)

        AKIPrintString(astring)

        astring = "\t\t Delay Time : " + str(estad2.DTa)

        AKIPrintString(astring)

        astring = "\t\t Speed : " + str(estad2.Sa)

        AKIPrintString(astring)

        astring = "\t\t Stop Time : " + str(estad2.STa)

        AKIPrintString(astring)

        astring = "\t\t NumStops : " + str(estad2.NumStops)

        AKIPrintString(astring)

        astring = "\t\t LongQueueAvg : " + str(estad2.LongQueueAvg)

        AKIPrintString(astring)

        astring = "\t\t LongQueueMax : " + str(estad2.LongQueueMax)

        AKIPrintString(astring)
  

    return 0
   


def update_avarege_Speed_db(dbName,speed):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    out = 1
    c.execute('CREATE TABLE IF NOT EXISTS averageSpeed(averageSpeed REAL, cycleNumber REAL)')
    c.execute('SELECT * FROM averageSpeed')
    for row in c.fetchall():
        print(row[1])   #must know with column is wanted
        out=(row[1])
    cycleNumber = out+1
   
    c.execute("""Update averageSpeed set averageSpeed = ? """,(speed,))
    c.execute("""Update averageSpeed set cycleNumber = ? """,(cycleNumber,))
    
    conn.commit()
    c.close()
    conn.close()

def update_historic_db(dbPath,speed, dalay, Total_distance_vehicles_inside,Total_time_vehicles_inside,opt_factors):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    unix = str(datetime.now().time())

    c.execute('CREATE TABLE IF NOT EXISTS hitoricReplicationTable(Time Text, AverageSpeed REAL, Delay REAL,Total_distance_vehicles_inside REAL , Total_time_vehicles_inside REAL, opt_fac_1 REAL,opt_fac_2 REAL ,opt_fac_3 REAL,opt_fac_4 REAL,opt_fac_5 REAL,opt_fac_6 REAL,opt_fac_7 REAL,opt_fac_8 REAL,opt_fac_9 REAL )')
    c.execute("INSERT INTO hitoricReplicationTable (Time , AverageSpeed , Delay ,Total_distance_vehicles_inside  , Total_time_vehicles_inside , opt_fac_1 ,opt_fac_2  ,opt_fac_3 ,opt_fac_4 ,opt_fac_5 ,opt_fac_6 ,opt_fac_7 ,opt_fac_8 ,opt_fac_9  ) VALUES (?,?,?,?,?  ,?,?,?,?,?,?,?,?,?)", (unix,speed, dalay, Total_distance_vehicles_inside,Total_time_vehicles_inside,opt_factors[0],opt_factors[1],opt_factors[2],opt_factors[3],opt_factors[4],opt_factors[5],opt_factors[6],opt_factors[7],opt_factors[8]))
    conn.commit()
    c.close()
    conn.close()

def read_from_db_parameters_path(pathOfDadaBase):

    connAux = sqlite3.connect(pathOfDadaBase)
    cAux = connAux.cursor()

    optList = []
    cAux.execute('SELECT * FROM Link')
    # data = c.fetchall()
    # print(data)
    for row in cAux.fetchall():
        optList.append(row[11])#must know with column is wanted
    print("The list of opt is: {}".format(optList))
    cAux.close()
    connAux.close()
    return optList

def getInfoFromdataBase(path):
    ### get info from sqlite
    ld = loader.Loader("C:\\Users\\Pedro Henrique Lenzi\\Desktop\\ECA - 20.1\\Estágio\\simulacao controle tuc caso menor\\small_arterial.sqlite")#load data base
    optFactor = ld.get_link_aimsun_map(12)# get column of data base that contais the opt factor
    print(" finished getInfoFromdataBase funtion ")
    return optFactor

def updateDataBase(optFactor):
    db_path = "C:\\Users\\Pedro Henrique Lenzi\\Desktop\\ECA - 20.1\\Estágio\\simulacao controle tuc caso menor\\small_arterial.sqlite"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    opt_1, opt_2, opt_3, opt_4, opt_5, opt_6, opt_7, opt_8, opt_9, opt_10, opt_11, opt_12, opt_13 = optFactor
    id=1
    f=0
    for i in optFactor:   #Goes through the list updating based on id number
        opt_novo = optFactor[f]
        c.execute("UPDATE Link set optFactor = ? where id = ?",(opt_novo,id))
        id = id +1
        f= f + 1
    
    conn.commit()  #save data
    conn.close     #close connection
    print(" finished updateDataBase funtion ")
    return 0