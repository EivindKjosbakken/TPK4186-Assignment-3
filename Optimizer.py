#group: 120, name: Eivind Kjosbakken

from Printer import Printer
from Simulator import Simulator



class Optimizer():
    def __init__(self):
        self.allStats = dict()



    def experimentalProtocol(self, timeStepToGoTo : int, numProductsInCatalog : int, numRobotsToTry : list, arrivalInterval : int, truckloadAndCustomerOrderRatesToTry : list, warehouseSizesToTry : list, fileNameToPrintOutputsTo : str):
        """returns a dictionary where the keys are warehouseStats-objects, and the value is a string describing the parameters for that simulation"""
        
        #using the parameters that are chosen 
        truckloadRates = truckloadAndCustomerOrderRatesToTry
        customerOrderRates = truckloadAndCustomerOrderRatesToTry
        robots = numRobotsToTry
        warehouseSizes = warehouseSizesToTry

        for i in range(len(truckloadAndCustomerOrderRatesToTry)):
            truckloadRate = truckloadRates[i]
            customerOrderRate = customerOrderRates[i]
            for numberOfRobots in robots:
                for size in warehouseSizes:
                    xSize = size[0]
                    if (xSize%6 != 0):
                        print("dimensioning xSize to be divisible by 6 (rounding downwards), so that all storages are accesible")
                        xSize -= xSize%6
                    ySize = size[1]
                    print("Doing", numberOfRobots, "robots,", "truckload/customerOrderRate:", truckloadRate, "/", customerOrderRate, "per", arrivalInterval ,"timeSteps", "xSize:", xSize, "ySize:", ySize)
                    simulator = Simulator()
                    wh, whStats = simulator.runSimulation(xSize, ySize, numberOfRobots, numProductsInCatalog, timeStepToGoTo, arrivalInterval, truckloadRate, customerOrderRate, False, False)
                    #write info about the experimental protocol
                    self.allStats[whStats] = f"{timeStepToGoTo} timeSteps, {numberOfRobots} robots, {truckloadRate} truckloadWeight/{arrivalInterval} timesteps, {customerOrderRate} customerOrderWeight/{arrivalInterval} timesteps. Warehouse size: ({xSize}, {ySize}). {numProductsInCatalog} different products"

        #write the results to file
        p = Printer()
        p.printExperimentalProtocolToFile(self.allStats, fileNameToPrintOutputsTo)

        return self.allStats

            

        

