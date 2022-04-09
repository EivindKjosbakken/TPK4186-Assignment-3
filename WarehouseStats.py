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
            raise Exception("the amount of truckloads in is not equal to the amount finished")
        totalTime = 0
        for i in range(len(self.truckloadArrivalTimes)):
            totalTime += (self.truckloadFinishTimes[i] - self.truckloadArrivalTimes[i])
        avgTime = totalTime/len(self.truckloadArrivalTimes)
        return avgTime

    def calculateAvgTimeToCompleteCustomerOrder(self):
        if len(self.customerOrderArrivalTimes) != len(self.customerOrderFinishTimes):
            raise Exception("the amount of customerOrders in is not equal to the amount finished")
        totalTime = 0
        for i in range(len(self.customerOrderArrivalTimes)):
            totalTime += (self.customerOrderFinishTimes[i] - self.customerOrderArrivalTimes[i])
        avgTime = totalTime/len(self.customerOrderArrivalTimes)
        return avgTime      

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