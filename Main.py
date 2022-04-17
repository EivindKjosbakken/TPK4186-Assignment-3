from Robot import Robot
from Warehouse import Warehouse
from Parameters import * 
from Simulator import * 

from Optimizer import Optimizer

p = Printer()

optimizer = Optimizer()

stats = optimizer.experimentalProtocol(20, 20)
p.printExperimentalProtocol(stats)




"""
#__________

sim = Simulator()     
numRobots = 2
xSize = 24  
ySize = 16 
timeStepToGoTo = 1785
maxTimeStep = 50000 
truckloadWeightPer5000 = 1000
customerOrderWeightPer5000 = 500
showTkinter = True
shouldPrint = True
wh, shouldBeInWarehouseAfterFinish = sim.runSimulation(xSize, ySize, numRobots, timeStepToGoTo, maxTimeStep, truckloadWeightPer5000, customerOrderWeightPer5000, showTkinter, shouldPrint)
#___________
#a = wh.getAllProductsAndAmountsInWarehouse()
#print("AFTER")
#for key, value in a.items():
#    print(key.getName(), ":", value)
"""


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