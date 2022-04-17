
import copy
from functools import partial
from logging import exception
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

#random.seed(0)

class Simulator():
    def __init__(self):
        self.timeStep = 0
        self.warehouseStats = None

    def runSimulation(self, xSize : int, ySize : int, numberOfRobots : int, timeStepToGoTO : int, maxTimeStep: int, truckloadSizePer5000Time : int, customerOrderSizePer5000Time : int,   displayWarehouse : bool, shouldPrint : bool):
        p = Printer() #TODO fjerne
        warehouse = Warehouse()
        self.warehouseStats = WarehouseStats(warehouse)

        rootWindow, canvas, zones = warehouse.makeWarehouseInTkinter(xSize, ySize)
        
        timeForReload = 5000 #let customerOrders/truckloads come in with 5000 timestep interval

        if (shouldPrint):
            p.printWarehouse(warehouse)

        robots = []
        for i in range(numberOfRobots):
            robot = Robot(f"robot{i}", warehouse)   
            robots.append(robot)
        warehouse.setRobots(robots)


        #if (truckloadSizePer5000Time - 10000 > customerOrderSizePer5000Time): #TODO implement something like this
        #    raise Exception("truckloadsize and customerordersize must be closer to eachother")
        
        #make sure the customerOrders are divisible by 5 (have 5 orders come in per 5000 timesteps)
        if (customerOrderSizePer5000Time%5 != 0):
            customerOrderSizePer5000Time -= customerOrderSizePer5000Time%5

        catalog = generateCatalog("catalog1", 5)
        self.warehouseStats.setCatalog(catalog)

        #choosing randomly the times the truckload and customerorder should come, doing 5 customerOrders and 1 truckload per 5000 timesteps
        customerOrderTimes = []
        for i in range(5):
            customerOrderTime = random.randint(0, timeForReload)
            customerOrderTimes.append(customerOrderTime)
        truckloadTime = random.randint(0, timeForReload)

        for i in range(timeStepToGoTO):
            self.addTruckloadsAndCustomerOrders(warehouse, catalog, shouldPrint, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
            
            if (shouldPrint):
                print("___TIMESTEP: ", i, " ____")
            warehouse.nextTimeStep(shouldPrint, self.warehouseStats)
            self.timeStep += 1

        gui = GUI()
        gui.createGUI(robots, canvas, zones, warehouse, rootWindow, displayWarehouse, shouldPrint, self.warehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
 
        return warehouse, self.warehouseStats


    def addTruckloadsAndCustomerOrders(self, warehouse : Warehouse, catalog : Catalog, shouldPrint : bool, maxTimeStep : int, timeForReload : int, truckloadTime : int, customerOrderTimes : int, truckloadSizePer5000Time : int, customerOrderSizePer5000Time : int):
        """add truckloads and customerOrders to warehouse in intervals, also stores all the truckloads and customerOrders in a stats class, so I can see how long each order took etc"""
        if (self.timeStep%timeForReload == truckloadTime and maxTimeStep-self.timeStep > maxTimeStep/5):
            truckload = generateTruckLoad(f"truckload{self.timeStep}", catalog, truckloadSizePer5000Time)
            warehouse.addTruckload(truckload)
            self.warehouseStats.addTruckload(copy.deepcopy(truckload))
            self.warehouseStats.addTruckloadArrivalTime(self.timeStep)
            if (shouldPrint):
                print("________ADDED TRUCKLOAD________")
        elif (self.timeStep%timeForReload in customerOrderTimes and maxTimeStep-self.timeStep > maxTimeStep/5):
            customerOrder = generateCustomerOrder(f"order{self.timeStep}", catalog, customerOrderSizePer5000Time//5)
            warehouse.addCustomerOrder(customerOrder)
            self.warehouseStats.addCustomerOrder(copy.deepcopy(customerOrder))
            self.warehouseStats.addCustomerOrderArrivalTime(self.timeStep)
            if (shouldPrint):
                print("_________ADDED CUSTOMERORDER___________")


#for running with tkinter

  