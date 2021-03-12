import os
import subprocess
import sys
import math
import sqlite3
# from scipy.optimize import minimize, rosen, rosen_der
from scipy.optimize import rosen, differential_evolution
import asyncio
from datetime import datetime
import math 



print("inicio script")

'''before running the code you must
# 1 - In the aimsun_script_main.py at the def function "def AAPIFinish()", with report the speed at end of simulation, add this: 
#       astring = "\t\t Speed : " + str(estad.Sa) 
        speedAvaregeSimulation = float(str(estad.Sa))
        update_avarege_Speed_db(db_output_replication_path,speedAvaregeSimulation)# update the database withlast simulation result


        and create a global variable def db_output_replication_path and links it with a path that will be used for a database. 
# 2 - Uptade the paths db_parameters_path and db_output_replication_path on this file with your path.

# 3 - Before running this code, you must to open a new prompt and call/run the tuc_interface.py

'''


##(open comunication tuc_interface.py)"C:/Users/Pedro Henrique Lenzi/AppData/Local/Microsoft/WindowsApps/python.exe" "c:/Users/Pedro Henrique Lenzi/Desktop/ECA - 20.1/Estágio/simulacao controle tuc caso menor/tuc_interface.py"

db_parameters_path = "C:\\Users\\Pedro Henrique Lenzi\\Desktop\\ECA - 20.1\\Estágio\\simulacao controle tuc caso menor\\small_arterial.sqlite"
db_output_replication_path = "C:\\Users\\Pedro Henrique Lenzi\\Desktop\\ECA - 20.1\\Estágio\\simulacao controle tuc caso menor\\OurputReplication.db"
historic_db_path = "C:\\Users\\Pedro Henrique Lenzi\\Desktop\\ECA - 20.1\\Estágio\\simulacao controle tuc caso menor\\HistoricReplicationdb.db"

speedAvaregeSimulation = 0
speed_funct_rounds = 0
t0 = datetime.now().time()







def update_parameters_db(pathDataBase,opt_factors):
    conn = sqlite3.connect(pathDataBase)
    c = conn.cursor()
    opt_1, opt_2, opt_3, opt_4, opt_5, opt_6, opt_7, opt_8, opt_9 = opt_factors
    id=1
    f=0
    for i in opt_factors:   #Itera a lista e atualiza os fatores de acordo com seu respectivo ID
        opt_novo = opt_factors[f]
        c.execute("UPDATE Link set optFactor = ? where id = ?",(opt_novo,id))
        if id == 1 or id == 9 or id == 6:
            if id == 1 or id == 6:
                id = id + 2
            else:
                id = id + 3
        else:
            id = id + 1
        
        f= f + 1
    conn.commit()
    c.close()
    conn.close()
      
    
def func_speed(opt_factors): 
    #update opt_fac values in DB
    update_parameters_db(db_parameters_path,opt_factors)
    print("Opt_fac: {}".format(str(opt_factors)))
    #call replication
    callReplication()
    #get the replication output
    speedAvaregeSimulation  = read_from_db_output_replication(db_output_replication_path,0)
    out = int(speedAvaregeSimulation)
    print("speedAvaregeSimulation: ",(str(speedAvaregeSimulation)))
    return (-1*out)


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


def read_from_db_output_replication(pathOfDadaBase,indx):
    connAux = sqlite3.connect(pathOfDadaBase)
    cAux = connAux.cursor()
    out = 0
    cAux.execute('SELECT * FROM averageSpeed')
    for row in cAux.fetchall():
        print(row[indx])   #must know with column is wanted
        out=(row[indx])
    cAux.close()
    connAux.close()
    print ("out Speed ={}".format(out))
    return(out)
    

async def callReplicationAsync():
    ommand_call_replication = str(" \"E:\Arquivo de Programas\Aimsun\Aimsun Next 20\aconsole.exe\" --project \"C:/Users/Pedro Henrique Lenzi/Desktop/ECA - 20.1/Estágio/simulacao controle tuc caso menor/test_arterial.ang\" --command execute --target 911")
    command_call_replication = str(""" "E:\Arquivo de Programas\Aimsun\Aimsun Next 20\aconsole.exe" --version""")

    
    subprocess.call(command_call_replication,shell=True)
    print("Finished async task")

def callReplication():
  
    #command_call_replication = str(" \"E:/Arquivo de Programas/Aimsun/Aimsun Next 20/Aimsun Next.exe\" --project \"C:/Users/Pedro Henrique Lenzi/Desktop/ECA - 20.1/Estágio/simulacao controle tuc caso menor/test_arterial.ang\" --command execute --target 911")
    command_call_replication = str(" \"E:/Arquivo de Programas/Aimsun/Aimsun Next 20/aconsole.exe\" --project \"C:/Users/Pedro Henrique Lenzi/Desktop/ECA - 20.1/Estágio/simulacao controle tuc caso menor/test_arterial.ang\" --command execute --target 911")

    subprocess.call(command_call_replication,shell=True)
    print("Finished task at the: ",datetime.now().time())


def update_avarege_Speed_db(dbName,speed,cycleNumber):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS averageSpeed(averageSpeed REAL, cycleNumber REAL)')
    c.execute("""Update averageSpeed set averageSpeed = ? """,(speed,))
    c.execute("""Update averageSpeed set cycleNumber = ? """,(cycleNumber,))
    
    conn.commit()
    c.close()
    conn.close()

def funct_teste(x):
    return ((x[0]**2)+(x[1]**2))

def main():
    update_avarege_Speed_db(db_output_replication_path,0,0)
    #optList = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
    #optList = [0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2]
    bnds = ((0.0, 5.0), (0.0, 5.0),(0.0, 5.0),(0.0, 5.0),(0.0, 5.0),(0.0, 5.0),(0.0, 5.0),(0.0, 5.0),(0.0, 5.0))
    # res = minimize(func_speed,optList,method='L-BFGS-B',tol=1e-3,bounds=bnds)
    # res = minimize(func_speed,optList,method='Nelder-Mead',tol=1e-5)
    result = differential_evolution(func_speed, bnds)
    print("result.x: ",result.x)
    print("result.fun",result.fun)
    print("The program started at ",datetime.now().time())
    #print ("Vel result:",float(func_speed(optList)))
    
    novos_fatores = res.x
    print("res.x: {}".format(res.x))

    print("the program ended at {}".format(datetime.now().time()))

def update_historic_db(dbPath,speed, dalay, Total_distance_vehicles_inside,Total_time_vehicles_inside,opt_factors):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    unix = str(datetime.now().time())
    print("opt q vai pra tabela> ",opt_factors)
    c.execute('CREATE TABLE IF NOT EXISTS hitoricReplicationTable(Time Text, AverageSpeed REAL, Delay REAL,Total_distance_vehicles_inside REAL , Total_time_vehicles_inside REAL, opt_fac_1 REAL,opt_fac_2 REAL ,opt_fac_3 REAL,opt_fac_4 REAL,opt_fac_5 REAL,opt_fac_6 REAL,opt_fac_7 REAL,opt_fac_8 REAL,opt_fac_9 REAL )')
    c.execute("INSERT INTO hitoricReplicationTable (Time , AverageSpeed , Delay ,Total_distance_vehicles_inside  , Total_time_vehicles_inside , opt_fac_1 ,opt_fac_2  ,opt_fac_3 ,opt_fac_4 ,opt_fac_5 ,opt_fac_6 ,opt_fac_7 ,opt_fac_8 ,opt_fac_9  ) VALUES (?,?,?,?,?  ,?,?,?,?,?,?,?,?,?)", (unix,speed, dalay, Total_distance_vehicles_inside,Total_time_vehicles_inside,
        opt_factors[0],opt_factors[1],opt_factors[2],opt_factors[3],opt_factors[4],opt_factors[5],opt_factors[6],opt_factors[7],opt_factors[8]))

    conn.commit()
    c.close()
    conn.close()


#(test)update_historic_db(historic_db_path,1,2,3,4,read_from_db_parameters_path(db_parameters_path))
main()
#(test)optList = [0.5000001,0.5000001,0.5000001,0.5000001,0.5000001,0.5000001,0.5000001,0.5000001,0.5000001]
#(test)optList = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]

#(test)update_parameters_db(db_parameters_path,optList)
#(test)callReplication()





