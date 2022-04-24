#group: 120, name: Eivind Kjosbakken

from Parameters import * 
from Simulator import * 

from Optimizer import Optimizer

p = Printer()

optimizer = Optimizer()


timeStepToGoTo = 150000
numProductsInCatalog = 120
numRobotsToTry = [1, 2, 5, 10]
truckloadAndCustomerOrderRatesToTry = [500, 1000, 3000, 10000]
arrivalInterval = 5000
warehouseSizesToTry = [(16, 24), (24, 30), (30, 30), (42, 42)]
fileNameToPrintOutputsTo = "outputs.txt"


stats = optimizer.experimentalProtocol(timeStepToGoTo, numProductsInCatalog, numRobotsToTry, arrivalInterval, truckloadAndCustomerOrderRatesToTry, warehouseSizesToTry, fileNameToPrintOutputsTo)



