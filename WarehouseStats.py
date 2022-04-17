from Parameters import *


#class to keep track of stats that are wanted from warehouse (how much time each customerOrder takes etc)
class WarehouseStats():
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.catalog = None

        self.allTruckloads = []
        self.allCustomerOrders = []

        self.truckloadArrivalTimes = []
        self.customerOrderArrivalTimes = []

        self.truckloadFinishTimes = []
        self.customerOrderFinishTimes = []

    def getWarehouse(self):
        return self.warehouse
    def getCatalog(self):
        return self.catalog
    def getAllTruckloads(self):
        return self.allTruckloads
    def getAllCustomerOrders(self):
        return self.allCustomerOrders
    def getTruckloadArrivalTimes(self):
        return self.truckloadArrivalTimes
    def getCustomerOrderArrivalTimes(self):
        return self.customerOrderArrivalTimes
    def getTruckloadFinishTimes(self):
        return self.truckloadFinishTimes
    def getCustomerOrderFinishTimes(self):
        return self.customerOrderFinishTimes

    def setCatalog(self, catalog):
        self.catalog = catalog


    def addTruckload(self, truckload):
        self.allTruckloads.append(truckload)
    def addCustomerOrder(self, customerOrder):
        self.allCustomerOrders.append(customerOrder)
    def addTruckloadArrivalTime(self, time : int):
        self.truckloadArrivalTimes.append(time)   
    def addCustomerOrderArrivalTime(self, time : int):
        self.customerOrderArrivalTimes.append(time)
    def addTruckloadFinishTime(self, time : int):
        self.truckloadFinishTimes.append(time)
    def addCustomerOrderFinishTime(self, time : int):
        self.customerOrderFinishTimes.append(time)
    

    def calculateAvgTimeToCompleteTruckload(self):
        """returns avg time used to complete a truckload, out of all the truckloads completed"""
        if len(self.truckloadArrivalTimes) != len(self.truckloadFinishTimes):
            return None
        length = 0
        #if not all truckloads was completed, just calculate times for the truckloads that was completed
        if (len(self.truckloadArrivalTimes) >= len(self.truckloadFinishTimes)):
            length = len(self.truckloadFinishTimes)
        else:
            length = len(self.truckloadArrivalTimes)
        totalTime = 0
        for i in range(length):
            totalTime += (self.truckloadFinishTimes[i] - self.truckloadArrivalTimes[i])
        if (len(self.truckloadArrivalTimes) !=0):
            avgTime = totalTime/len(self.truckloadArrivalTimes)

        return avgTime

    def calculateAvgTimeToCompleteCustomerOrder(self):
        if len(self.customerOrderArrivalTimes) != len(self.customerOrderFinishTimes):
            return None
            #raise Exception("the amount of customerOrders in is not equal to the amount finished")
        length = 0
        if (len(self.customerOrderArrivalTimes) >= len(self.customerOrderFinishTimes)):
            length = len(self.customerOrderFinishTimes)
        else:
            length = len(self.customerOrderArrivalTimes)
        totalTime = 0
        for i in range(length):
            totalTime += (self.customerOrderFinishTimes[i] - self.customerOrderArrivalTimes[i])
        avgTime = totalTime/len(self.customerOrderArrivalTimes)
        return avgTime      

    def calculateTotalWeightOfCustomerOrders(self):
        totalWeight = 0
        for customerOrder in self.allCustomerOrders:
            totalWeight += customerOrder.calculateTotalWeight()
        return totalWeight

    def calculateTotalWeightOfTruckloads(self):
        totalWeight = 0
        for truckload in self.allTruckloads:
            totalWeight += truckload.calculateTotalWeight()
        return totalWeight

    def getAllTruckloadsInOneDict(self):
        """returns dictionar of all truckloads, the keys are strings (not product objects)"""
        allTruckloadsDict = dict()
        for truckload in self.allTruckloads:
            for product, amount in truckload.getLoad().items():
                addToDict(allTruckloadsDict, product.getName(), amount)
        return allTruckloadsDict

    def getAllCustomerOrdersInOneDict(self):
        """return dictionary of all customerOrders, the keys are strings (not product objects)"""
        allCustomerOrdersDict = dict()
        for customerOrder in self.allCustomerOrders:
            for product, amount in customerOrder.getOrder().items():
                addToDict(allCustomerOrdersDict, product.getName(), amount)
        return allCustomerOrdersDict

    def getProductsFromTruckloadsMinusCustomerOrders(self):
        """for testing purposes, make sure what goes into warehouse = what is in warehouse"""
        allTruckloads = self.getAllTruckloadsInOneDict()
        allCustomerOrders = self.getAllCustomerOrdersInOneDict()

        for productName, amount in allCustomerOrders.items():
            removeFromDict(allTruckloads, productName, amount)
        return allTruckloads