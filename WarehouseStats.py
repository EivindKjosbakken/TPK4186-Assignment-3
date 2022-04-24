#group: 120, name: Eivind Kjosbakken

from Parameters import *


#class to keep track of stats that are wanted from warehouse (how much time each customerOrder takes etc)
class WarehouseStats():
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.catalog = None
        self.wasFull = False #True if warehouse got full and couldnt place any products, and did not have enough product t 

        self.allTruckloadsThatArrived = []
        self.allCustomerOrdersThatArrived = []

        self.truckloadArrivalTimes = []
        self.customerOrderArrivalTimes = []

        self.truckloadFinishTimes = []
        self.customerOrderFinishTimes = []

    def getWarehouse(self):
        return self.warehouse
    def getCatalog(self):
        return self.catalog
    def getWasFull(self):
        return self.wasFull
    def getAllTruckloadsThatArrived(self):
        """returns all the truckloads that arrived in warehouse during simulation"""
        return self.allTruckloadsThatArrived
    def getAllCustomerOrdersThatArrived(self):
        """returns all the customerOrders that arrived in warehouse during simulation"""
        return self.allCustomerOrdersThatArrived
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
    def setWasFull(self, wasFull : bool):
        self.wasFull = wasFull


    def addTruckload(self, truckload):
        self.allTruckloadsThatArrived.append(truckload)
    def addCustomerOrder(self, customerOrder):
        self.allCustomerOrdersThatArrived.append(customerOrder)
    def addTruckloadArrivalTime(self, time : int):
        self.truckloadArrivalTimes.append(time)   
    def addCustomerOrderArrivalTime(self, time : int):
        self.customerOrderArrivalTimes.append(time)
    def addTruckloadFinishTime(self, time : int):
        self.truckloadFinishTimes.append(time)
    def addCustomerOrderFinishTime(self, time : int):
        self.customerOrderFinishTimes.append(time)
    

    def calculateAvgTimeToCompleteTruckload(self):
        """returns average time used to complete a truckload, out of all the truckloads completed"""
        totalTime = 0
        for i in range(len(self.truckloadFinishTimes)):
            totalTime += (self.truckloadFinishTimes[i] - self.truckloadArrivalTimes[i])
        avgTime = 0
        if (len(self.truckloadFinishTimes) !=0):
            avgTime = totalTime/len(self.truckloadFinishTimes)
        else:
            print("0 arrival")
            avgTime = 0

        return avgTime

    def calculateAvgTimeToCompleteCustomerOrder(self):
        """returns average time used to complete all the customerOrders that was completed"""
        totalTime = 0
        for i in range(len(self.customerOrderFinishTimes)):
            totalTime += (self.customerOrderFinishTimes[i] - self.customerOrderArrivalTimes[i])
        avgTime = 0
        if (len(self.customerOrderFinishTimes) == 0):
            print("0 completed")
            avgTime = 0
        else:
            avgTime = totalTime/len(self.customerOrderFinishTimes)
        return avgTime      

    def calculateTotalWeightOfCustomerOrders(self):
        """returns total weight contained in all the customerOrders the warehouse received"""
        totalWeight = 0
        for customerOrder in self.allCustomerOrdersThatArrived:
            totalWeight += customerOrder.calculateTotalWeight()
        return totalWeight

    def calculateTotalWeightOfTruckloads(self):
        """returns total weight contained in all the truckloads the warehouse received"""
        totalWeight = 0
        for truckload in self.allTruckloadsThatArrived:
            totalWeight += truckload.calculateTotalWeight()
        return totalWeight
 
