from Simulator import Simulator


class Optimizer():
    def __init__(self):
        self.allStats = dict()



    def experimentalProtocol(self, numRobots, numTruckloadsAndCustomerOrders):
        """returns a where the keys are warehouseStats-objects, and the value is a string describing the parameters for that simulation"""
        truckloadRates = [1000*i for i in range(1, numTruckloadsAndCustomerOrders+1)] 
        customerOrderRates = [500*i for i in range(1,numTruckloadsAndCustomerOrders+1)]

        #trying with everything from 1 robot to 40 robots
        robots = [i for i in range(1, numRobots+1)] 


        #for different robots from 1 to 5000
        for i in range(numTruckloadsAndCustomerOrders):
            truckloadRate = truckloadRates[i]
            customerOrderRate = customerOrderRates[i]
            for numberOfRobots in robots:
                print("Doing", numberOfRobots, "robots", "truckload/customerOrderRate:", truckloadRate, customerOrderRate)
                simulator = Simulator()
                wh, whStats = simulator.runSimulation(24, 16, numberOfRobots, 50000, 50000, truckloadRate,
                customerOrderRate, False, False)
                self.allStats[whStats] = f"{numberOfRobots} robots, 1000 truckloadweight/5000 timesteps, 750 customerOrderweight/5000 timesteps"

        return self.allStats

            

        

