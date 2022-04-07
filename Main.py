from Robot import Robot
from Warehouse import Warehouse
from Parameters import * 
from Simulator import * 



#__________

sim = Simulator()     
numRobots = 2
xSize = 24
ySize = 16 
timeSteps = 3000 # 2300 funka, ferdig etter 2417
wh = sim.runSimulation(xSize, ySize, numRobots, timeSteps, True)
#___________
counter = 0


"""
def printProdDict(prods):
    for key, value in prods.items():
        print(key.getName(), ":", value, end= ", ")

all = wh.getAllProductsAndAmountsInWarehouse()
print()
print("ALL PRODUCTS IN WAREHOUSE:")
printProdDict(all)
currentLoad = wh.getTruckload().getLoad()
print("TRUCKLOAD IS:")
printProdDict(currentLoad)
print()
"""