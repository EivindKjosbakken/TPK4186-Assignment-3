
import copy
from functools import partial
from CustomerOrder import CustomerOrder
from Printer import Printer
from Product import Product
from Robot import Robot
from Truckload import Truckload
from Warehouse import Warehouse
from Parameters import *
from tkinter import *


class Simulator():
    def __init__(self):
        self.timeStep = 0
        

    def runSimulation(self, xSize : int, ySize : int, numberOfRobots : int, maxTimeStep : int, truckloadSizePer5000Time : int, customerOrderSizePer5000Time : int,   displayWarehouse : bool, shouldPrint : bool):
        if numberOfRobots>50:
            print("Can't have more than 50 robots, that means chaos in the warehouse")
        warehouse = Warehouse()
        rootWindow, canvas, zones = warehouse.makeWarehouseInTkinter(xSize, ySize)
        if (shouldPrint):
            printer = Printer()
            printer.printWarehouse(warehouse)

        robots = []
        for i in range(numberOfRobots):
            robot = Robot(f"robot{i}", warehouse)   
            robots.append(robot)
        warehouse.setRobots(robots)

        """ """
        #generating truckorders and customerorders:
        catalog = generateCatalog("catalog1", 5)
        truckload = generateTruckLoad("truckload", catalog, 23000)
        p = Printer()
        warehouse.addTruckload(truckload)
        #p.printTruckload(truckload)

        shouldBeInWarehouseAfterFinish = dict()
        for product, amount in truckload.getLoad().items():
            addToDict(shouldBeInWarehouseAfterFinish, product.getName(), amount)
        
        allCustOrders = dict()
        for i in range(15):
            customerOrder = generateCustomerOrder(f"customerOrder{i}", catalog, 500)
            warehouse.addCustomerOrder(customerOrder)
            #p.printCustomerOrder(customerOrder)
            for product, amount in customerOrder.getOrder().items():
                addToDict(allCustOrders, product.getName(), amount)

        #for testing purposes:
        for product, amount in allCustOrders.items():
            removeFromDict(shouldBeInWarehouseAfterFinish, product, amount)
    
        for i in range(maxTimeStep):
            #print()
            if (shouldPrint):
                print("___TIMESTEP: ", i, " ____")
            warehouse.nextTimeStep(shouldPrint)
            self.timeStep += 1

        self.createGUI(robots, canvas, zones, warehouse, rootWindow, displayWarehouse)

        return warehouse, shouldBeInWarehouseAfterFinish




#for running with tkinter
    def createGUI(self, robots : list, canvas : Canvas, zones : list, warehouse : Warehouse, rootWindow, displayWarehouse : bool):
        self.updateRobotPosition(robots, canvas, zones)
        canvas.create_text(600, 20, text="Yellow cells: where robots are, grey cells: where storage cells are, green cells: where moving cells are. Blue are not cells in the warehouse, black are start/end cells (can not see robots when in start/endcells", fill="black", font=('Helvetica 8 bold'))
        canvas.pack()

        #adding button for going to next timestep, inside tkinter application
        frame = Frame(rootWindow)
        
        button1 = Button(frame, text = "Go to next timestep", command=partial(self.nextTimeStepTkinter, warehouse, robots, canvas, zones)) 
        button1.pack()
        button2 = Button(frame, text = "Go to 10th next timestep", command=partial(self.next10TimeStepsTkinter, warehouse, robots, canvas, zones)) 
        button2.pack()

        frame.pack()
        if (displayWarehouse):
            rootWindow.mainloop()

    def nextTimeStepTkinter(self, warehouse : Warehouse, robots : list, canvas : Canvas, zones : list):
        print(f"\n ____TIMESTEP {self.timeStep}____")
        self.timeStep+=1
        warehouse.nextTimeStep()
        self.updateRobotPosition(robots, canvas, zones)

        
    def next10TimeStepsTkinter(self, warehouse : Warehouse, robots : list, canvas : Canvas, zones : list):
        for i in range(10):
            print(f"\n ____TIMESTEP {self.timeStep}____")
            self.timeStep+=1
            warehouse.nextTimeStep()
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


  