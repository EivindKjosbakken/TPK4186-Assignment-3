
import copy
from functools import partial
from logging import exception
from CustomerOrder import CustomerOrder
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

        if numberOfRobots>50:
            print("Can't have more than 50 robots, that means chaos in the warehouse")
        
        rootWindow, canvas, zones = warehouse.makeWarehouseInTkinter(xSize, ySize)
        if (shouldPrint):
            printer = Printer()
            printer.printWarehouse(warehouse)

        robots = []
        for i in range(numberOfRobots):
            robot = Robot(f"robot{i}", warehouse)   
            robots.append(robot)
        warehouse.setRobots(robots)


        #if (truckloadSizePer5000Time - 10000 > customerOrderSizePer5000Time): #TODO implement something like this
        #    raise Exception("truckloadsize and customerordersize must be closer to eachother")
        if (customerOrderSizePer5000Time%5 != 0):
            customerOrderSizePer5000Time -= customerOrderSizePer5000Time%5

        timeForReload = 5000
        catalog = generateCatalog("catalog1", 5)
        self.warehouseStats.setCatalog(catalog)
        #choosing times the truckload and customerorder should come
        customerOrderTimes = []
        for i in range(5):
            customerOrderTime = random.randint(0, timeForReload)
            customerOrderTimes.append(customerOrderTime)
        truckloadTime = random.randint(0, timeForReload)

        #allCustOrders = dict()
        #shouldBeInWarehouseAfterFinish = dict()

        for i in range(timeStepToGoTO):

            self.addTruckloadsAndCustomerOrders(warehouse, catalog, shouldPrint, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
            
            if (shouldPrint):
                print("___TIMESTEP: ", i, " ____")
            warehouse.nextTimeStep(shouldPrint, self.warehouseStats)
            self.timeStep += 1


        self.createGUI(robots, canvas, zones, warehouse, rootWindow, displayWarehouse, shouldPrint, self.warehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
    
        #for running the tests (makes sure that what goes in from the truckloads minus what goes out from the customerOrders, is equal to the amount of products in the warehouse)
        #for productName, amount in allCustOrders.items():
        #    removeFromDict(shouldBeInWarehouseAfterFinish, productName, amount)
 
        return warehouse, self.warehouseStats#shouldBeInWarehouseAfterFinish


    
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
    def createGUI(self, robots : list, canvas : Canvas, zones : list, warehouse : Warehouse, rootWindow, displayWarehouse : bool, shouldPrint : bool, warehouseStats : WarehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time):
        self.updateRobotPosition(robots, canvas, zones)
        canvas.create_text(600, 20, text="Yellow cells: where robots are, grey cells: where storage cells are, green cells: where moving cells are. Blue are not cells in the warehouse, black are start/end cells (can not see robots when in start/endcells", fill="black", font=('Helvetica 8 bold'))
        canvas.pack()

        #adding button for going to next timestep, inside tkinter application
        frame = Frame(rootWindow)
        
        button1 = Button(frame, text = "Go to next timestep", command=partial(self.nextTimeStepTkinter, warehouse, robots, canvas, zones, shouldPrint, warehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)) 
        button1.pack()
        button2 = Button(frame, text = "Go to 10th next timestep", command=partial(self.next10TimeStepsTkinter, warehouse, robots, canvas, zones, shouldPrint, warehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)) 
        button2.pack()

        frame.pack()
        if (displayWarehouse):
            rootWindow.mainloop()

    def nextTimeStepTkinter(self, warehouse : Warehouse, robots : list, canvas : Canvas, zones : list, shouldPrint : bool, warehouseStats : WarehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time):
        self.addTruckloadsAndCustomerOrders(warehouse, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
        print(f"\n ____TIMESTEP {self.timeStep}____")
        self.timeStep+=1
        warehouse.nextTimeStep(shouldPrint, warehouseStats)
        self.updateRobotPosition(robots, canvas, zones)


    def next10TimeStepsTkinter(self, warehouse : Warehouse, robots : list, canvas : Canvas, zones : list, shouldPrint : bool, warehouseStats : WarehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time):
        for i in range(10):
            self.addTruckloadsAndCustomerOrders(warehouse, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
            print(f"\n ____TIMESTEP {self.timeStep}____")
            self.timeStep+=1
            warehouse.nextTimeStep(shouldPrint, warehouseStats)
            self.updateRobotPosition(robots, canvas, zones)

    def updateRobotPosition(self, robots : list, canvas : Canvas, zones : list):
        robotPositions = []
        for robot in robots:
            currCell = robot.getCurrentCell()
            if (currCell != None):
                x, y = currCell.getCoordinates()
                robotPositions.append((x,y))

        for robot in robots:
            (x,y) = robot.getCurrentCell().getCoordinates()
            canvas.itemconfig(zones[y-1][x-1], fill="yellow") #-1 because its indexes!
            prevCell = robot.getPreviousCell()
            if (prevCell != None):
                cellType = prevCell.getCellType()
                prevX, prevY = prevCell.getCoordinates()
                if ((prevX, prevY) not in robotPositions): #if another robot is not at same position
                    if (cellType=="moveLeft" or cellType=="moveRight" or cellType=="moveUp" or cellType=="moveDown"):
                        canvas.itemconfig(zones[prevY-1][prevX-1], fill="green") #-1 because its indexes!
                    else:
                        canvas.itemconfig(zones[prevY-1][prevX-1], fill="white") 


  