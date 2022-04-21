from Robot import Robot
from Warehouse import Warehouse
from Parameters import * 
from Simulator import * 

from Optimizer import Optimizer

p = Printer()

optimizer = Optimizer()


numTimeSteps = 300000
numProductsInCatalog = 30
numRobotsToTry = [13, 5, 7, 10, 15, 20, 30, 40]
truckloadAndCustomerOrderRatesToTry = [500, 1000, 2000, 4000, 6000, 8000, 12000, 20000]
warehouseSizesToTry = [(8, 12), (24, 16), (30, 30)]
stats = optimizer.experimentalProtocol(numTimeSteps, numProductsInCatalog, numRobotsToTry, truckloadAndCustomerOrderRatesToTry, warehouseSizesToTry)
p.printExperimentalProtocol(stats)

#sim = Simulator()
#warehouse, whStats = sim.runSimulation(24, 18, 3, 5, 1000, 50000, 10000, 500, True, False)

