from tqdm import trange
from Simulator import Simulator


class Optimizer():
    def __init__(self):
        self.allStats = dict()



    def experimentalProtocol(self, numTimesteps : int, numProductsInCatalog : int, numRobotsToTry : list, truckloadAndCustomerOrderRatesToTry : list, warehouseSizesToTry : list):
        """returns a dictionary where the keys are warehouseStats-objects, and the value is a string describing the parameters for that simulation"""
        truckloadRates = truckloadAndCustomerOrderRatesToTry
        customerOrderRates = truckloadAndCustomerOrderRatesToTry

        #trying with everything from 1 robot to numRobots
        robots = numRobotsToTry

        warehouseSizes = warehouseSizesToTry

        for i in range(len(truckloadAndCustomerOrderRatesToTry)):
            truckloadRate = truckloadRates[i]
            customerOrderRate = customerOrderRates[i]
            for numberOfRobots in robots:
                for size in warehouseSizes:
                    xSize = size[0]
                    ySize = size[1]
                    print("Doing", numberOfRobots, "robots,", "truckload/customerOrderRate:", truckloadRate, "/", customerOrderRate, ", xSize:", xSize, "ySize:", ySize)
                    simulator = Simulator()
                    wh, whStats = simulator.runSimulation(xSize, ySize, numberOfRobots, numProductsInCatalog, numTimesteps, numTimesteps, truckloadRate,
                    customerOrderRate, False, False)

                    #write info about the experimental protocol
                    self.allStats[whStats] = f"{numTimesteps} timeSteps, {numberOfRobots} robots, {truckloadRate} truckloadWeight/5000 timesteps, {customerOrderRate} customerOrderWeight/5000 timesteps. Warehouse size: ({xSize}, {ySize}). {numProductsInCatalog} different products"

        return self.allStats

            

        

