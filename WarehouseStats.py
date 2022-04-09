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


    def setCatalog(self, catalog):
        self.catalog = catalog

    def addTruckload(self, truckload):
        self.allTruckloads.append(truckload)
    def addCustomerOrder(self, customerOrder):
        self.allCustomerOrders.append(customerOrder)
    def addTruckloadArrival(self, time : int):
        self.truckloadArrivalTimes.append(time)   
    def addCustomerOrderArrival(self, time : int):
        self.customerOrderArrivalTimes.append(time)
    def addTruckloadFinishTime(self, time : int):
        self.truckloadFinishTimes.append(time)
    def addCustomerOrderFinishTime(self, time : int):
        self.customerOrderFinishTimes.append(time)
    
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



    def getAllTruckloadsInOneDict(self):
        allTruckloadsDict = dict()
        print("Tloads:", self.allTruckloads)
        for truckload in self.allTruckloads:
            for product, amount in truckload.getLoad().items():
                addToDict(allTruckloadsDict, product, amount)
                print("prod:", product.getName(), "amount:", amount)
        return allTruckloadsDict

    def getAllCustomerOrdersInOneDict(self):
        allCustomerOrdersDict = dict()
        for customerOrder in self.allCustomerOrders:
            for product, amount in customerOrder.getOrder().items():
                addToDict(allCustomerOrdersDict, product, amount)
        return allCustomerOrdersDict

    def getProductsFromTruckloadsMinusCustomerOrders(self):
        """for testing purposes, make sure what goes into warehouse = what is in warehouse"""
        allTruckloads = self.getAllTruckloadsInOneDict()
        allCustomerOrders = self.getAllCustomerOrdersInOneDict()
        print("WHEN GETTING", allTruckloads, allCustomerOrders)
        for product, amount in allCustomerOrders.items():
            removeFromDict(allTruckloads, product, amount)
        return allTruckloads