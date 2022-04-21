
import copy
from functools import partial
from CustomerOrder import CustomerOrder
from GUI import GUI
from Printer import Printer
from Product import Product
from Robot import Robot
from Truckload import Truckload
from Warehouse import Warehouse
from Parameters import *
from tkinter import *
from WarehouseStats import WarehouseStats
from tqdm import trange

class Simulator():
    def __init__(self):
        self.timeStep = 0
        self.warehouseStats = None

    def getTimeStep(self):
        return self.timeStep
    def getWarehouseStats(self):
        return self.warehouseStats
    def setTimeStep(self, timeStep : int):
        self.timeStep = timeStep
    def setWarehouseStats(self, warehouseStats : WarehouseStats):
        self.warehouseStats = warehouseStats
    
    def increaseTimeStep(self):
        self.timeStep+=1

    def runSimulation(self, xSize : int, ySize : int, numberOfRobots : int, numProductsInCatalog : int, timeStepToGoTO : int, maxTimeStep: int, truckloadSizePer5000Time : int, customerOrderSizePer5000Time : int,   displayWarehouse : bool, shouldPrint : bool):
        """returns the warehouse of the simulation, and the warehouseStats of the simulation"""
        if (xSize < 6 or ySize < 6):
            raise Exception("Warehouse dimension must be atleast 6 in x direction, and 6 in y direction (else the warehouse cant have a reasonable shape)")

  
        p = Printer()
        warehouse = Warehouse()
        self.warehouseStats = WarehouseStats(warehouse)

        rootWindow, canvas, zones = warehouse.makeWarehouseInTkinter(xSize, ySize)
        allStorageCells = warehouse.getAllStorageCells()
        if (len(allStorageCells)*2 < numProductsInCatalog):
            raise Exception("Number of products exceeds the number of shelves in the warehouse, will not be able to store all, try bigger warehouse or fewer unique products")
            
        timeForReload = 5000 #let customerOrders/truckloads come in with 5000 timestep interval

        if (shouldPrint):
            p.printWarehouse(warehouse)

        robots = []
        for i in range(numberOfRobots):
            robot = Robot(f"robot{i}", warehouse)   
            robots.append(robot)
        warehouse.setRobots(robots)


        #make sure the customerOrders are divisible by 5 (have 5 orders come in per 5000 timesteps)
        if (customerOrderSizePer5000Time%5 != 0):
            customerOrderSizePer5000Time -= customerOrderSizePer5000Time%5

        catalog = generateCatalog("catalog1", numProductsInCatalog)
        self.warehouseStats.setCatalog(catalog)

        #choosing randomly the times the truckload and customerorder should come, doing 5 customerOrders and 1 truckload per 5000 timesteps
        random.seed(6) #TODO fjerne
        customerOrderTimes = []
        for i in range(5):
            customerOrderTime = random.randint(0, timeForReload)
            customerOrderTimes.append(customerOrderTime)
        truckloadTime = random.randint(0, timeForReload)
        print("CUST TIMES:", customerOrderTimes)
        for i in trange(timeStepToGoTO): #trange so I can see how long is left of running time, from tqdm package
            self.addTruckloadsAndCustomerOrders(warehouse, catalog, shouldPrint, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
            
            if (shouldPrint):
                print("___TIMESTEP: ", i, " ____")
            warehouse.nextTimeStep(shouldPrint, self.warehouseStats)
            self.timeStep += 1

        gui = GUI(self)
        gui.createGUI(robots, canvas, zones, warehouse, rootWindow, displayWarehouse, shouldPrint, self.warehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
 
        return warehouse, self.warehouseStats


    def addTruckloadsAndCustomerOrders(self, warehouse : Warehouse, catalog : Catalog, shouldPrint : bool, maxTimeStep : int, timeForReload : int, truckloadTime : int, customerOrderTimes : list, truckloadSizePer5000Time : int, customerOrderSizePer5000Time : int):
        """add truckloads and customerOrders to warehouse in intervals, also stores all the truckloads and customerOrders in a stats class, so I can see how long each order took etc"""
        if ((self.timeStep%timeForReload == truckloadTime and self.timeStep>5000) or (self.timeStep==0)):
            truckload = generateTruckLoad(f"truckload{self.timeStep}", catalog, truckloadSizePer5000Time)
            warehouse.addTruckload(truckload)
            self.warehouseStats.addTruckload(copy.deepcopy(truckload))
            self.warehouseStats.addTruckloadArrivalTime(self.timeStep)
            if (shouldPrint):
                print("________ADDED TRUCKLOAD________")
        elif (self.timeStep%timeForReload in customerOrderTimes):
            customerOrder = generateCustomerOrder(f"order{self.timeStep}", catalog, customerOrderSizePer5000Time//5)
            warehouse.addCustomerOrder(customerOrder)
            self.warehouseStats.addCustomerOrder(copy.deepcopy(customerOrder))
            self.warehouseStats.addCustomerOrderArrivalTime(self.timeStep)
            if (shouldPrint):
                print("_________ADDED CUSTOMERORDER___________")




  