
from functools import partial
from Product import Product
from Robot import Robot
from Truckload import Truckload
from Warehouse import Warehouse

from tkinter import *


class Simulator():
    def __init__(self):
        self.timeStep = 0
        

    def runSimulation(self, xSize : int, ySize : int, numberOfRobots : int, maxTimeStep : int, displayWarehouse : bool):
        warehouse = Warehouse()
        #warehouse.createWarehouse(xSize, ySize)
        rootWindow, canvas, zones = warehouse.makeWarehouseInTkinter(xSize, ySize)
        warehouse.printWarehouse()
        robots = []
        for i in range(numberOfRobots):
            robot = Robot(f"robot{i}", warehouse)   
            robots.append(robot)
        warehouse.setRobots(robots)
        #hardcoding Truckload for now
        cheese = Product("cheese", 10)
        chair = Product("chair", 10)
        table = Product("table", 19)
        pen = Product("pen", 3)
        truckload = Truckload("t", 100000)
        load = {cheese : 156, chair : 158, table : 156, pen : 200}
        truckload.setLoad(load)
        warehouse.setTruckload(truckload)
        print("_____", warehouse.getTruckload().getLoad())
        for i in range(maxTimeStep):
            print()
            print("___TIMESTEP: ", i, " ____")
            warehouse.nextTimeStep()
            self.timeStep += 1

        self.updateRobotPosition(robots, canvas, zones)

        canvas.create_text(600, 20, text="Yellow cells: where robots are, grey cells: where storage cells are, green cells: where moving cells are. Blue are not cells in the warehouse, black are start/end cells (can not see robots when in start/endcells", fill="black", font=('Helvetica 8 bold'))
        canvas.pack()
        
        #adding button for going to next timestep, inside tkinter application
        frame = Frame(rootWindow)
        frame.pack()
        button1 = Button(frame, text = "Go to next timestep", command=partial(self.nextTimeStepTkinter, warehouse, robots, canvas, zones)) 
        button1.pack()
        if (displayWarehouse):
            rootWindow.mainloop()
        return warehouse

    def nextTimeStepTkinter(self, warehouse : Warehouse, robots : list, canvas : Canvas, zones : list):
        print(f"\n ____TIMESTEP {self.timeStep}____")
        self.timeStep+=1
        warehouse.nextTimeStep()
        self.updateRobotPosition(robots, canvas, zones)
        if (robots[0].previousCell!=None):
            print("PREV CELL: ", robots[0].previousCell.getCoordinates())
        else:
            print("PREV CELL NOT AVAIL")


    def updateRobotPosition(self, robots : list, canvas : Canvas, zones : list):
        robotPositions = []
        for robot in robots:
            currCell = robot.getCurrentCell()
            if (currCell != None):
                x, y = currCell.getCoordinates()
                robotPositions.append((x,y))

        for robot in robots:
            (x,y) = robot.getCurrentCell().getCoordinates()
            print("zones: ", zones[y-1][x-1])
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

            else:
                print("ROBOT DID NOT HAVE PREV")
  